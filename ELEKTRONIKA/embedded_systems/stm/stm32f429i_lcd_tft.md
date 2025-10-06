# STM32F429I - LCD-TFT i Interfejs Graficzny

## 🖥️ LCD-TFT Controller (LTDC)

### Wprowadzenie
STM32F429I posiada wbudowany kontroler LCD-TFT (LTDC - LCD TFT Display Controller) z akceleratorem graficznym DMA2D (Chrom-ART), umożliwiający bezpośrednie sterowanie wyświetlaczami TFT bez zewnętrznego kontrolera.

### Charakterystyka LTDC

| Parametr | Wartość |
|----------|---------|
| Rozdzielczość max | 1024×768 (teoretyczna) |
| Warstwy (layers) | 2 niezależne |
| Formaty pikseli | RGB888, RGB565, ARGB8888, etc. |
| DMA2D | Akcelerator graficzny 2D (Chrom-ART) |
| CLUT | Color Look-Up Table (256 kolorów) |
| Blending | Alpha blending między warstwami |
| Częstotliwość pikseli | Do 83 MHz |

### Architektura LTDC

```
┌──────────────────────────────────────────────┐
│              LTDC Controller                 │
│                                              │
│  ┌───────────┐         ┌───────────┐        │
│  │  Layer 0  │         │  Layer 1  │        │
│  │ (tło)     │         │ (pierwszy │        │
│  │           │         │  plan)    │        │
│  └─────┬─────┘         └─────┬─────┘        │
│        │                     │              │
│        └──────────┬──────────┘              │
│                   │                         │
│            ┌──────▼──────┐                  │
│            │   Blending  │                  │
│            │   Engine    │                  │
│            └──────┬──────┘                  │
│                   │                         │
│            ┌──────▼──────┐                  │
│            │  Output     │                  │
│            │  Timing     │──────▶ RGB/LVDS  │
│            └─────────────┘                  │
└──────────────────────────────────────────────┘
```

## 🔧 Konfiguracja podstawowa LTDC

### Timing i sygnały synchronizacji

```c
/**
 * @brief  Konfiguracja LTDC dla wyświetlacza 480x272
 */
LTDC_HandleTypeDef hltdc;

void LTDC_Init(void)
{
    // Parametry timingowe dla 480x272
    hltdc.Instance = LTDC;
    
    // Timing configuration
    hltdc.Init.HorizontalSync = 40;      // HSYNC width - 1
    hltdc.Init.VerticalSync = 9;         // VSYNC height - 1
    hltdc.Init.AccumulatedHBP = 42;      // HSYNC + HBP - 1
    hltdc.Init.AccumulatedVBP = 11;      // VSYNC + VBP - 1
    hltdc.Init.AccumulatedActiveW = 522; // HSYNC + HBP + Width - 1
    hltdc.Init.AccumulatedActiveH = 283; // VSYNC + VBP + Height - 1
    hltdc.Init.TotalWidth = 524;         // HSYNC + HBP + Width + HFP - 1
    hltdc.Init.TotalHeigh = 285;         // VSYNC + VBP + Height + VFP - 1
    
    // Polarity configuration
    hltdc.Init.HSPolarity = LTDC_HSPOLARITY_AL;  // Active Low
    hltdc.Init.VSPolarity = LTDC_VSPOLARITY_AL;
    hltdc.Init.DEPolarity = LTDC_DEPOLARITY_AL;
    hltdc.Init.PCPolarity = LTDC_PCPOLARITY_IPC;
    
    // Background color (RGB)
    hltdc.Init.Backcolor.Blue = 0;
    hltdc.Init.Backcolor.Green = 0;
    hltdc.Init.Backcolor.Red = 0;
    
    if (HAL_LTDC_Init(&hltdc) != HAL_OK) {
        Error_Handler();
    }
}
```

### Konfiguracja warstwy (Layer)

```c
/**
 * @brief  Konfiguracja Layer 0 (RGB565)
 */
#define LCD_WIDTH  480
#define LCD_HEIGHT 272
#define FRAMEBUFFER_SIZE (LCD_WIDTH * LCD_HEIGHT * 2)  // 2 bytes per pixel dla RGB565

// Framebuffer w SDRAM lub dużej SRAM
__attribute__((section(".sdram"))) uint16_t framebuffer[LCD_WIDTH * LCD_HEIGHT];

void LTDC_Layer_Init(void)
{
    LTDC_LayerCfgTypeDef pLayerCfg = {0};
    
    pLayerCfg.WindowX0 = 0;
    pLayerCfg.WindowX1 = LCD_WIDTH;
    pLayerCfg.WindowY0 = 0;
    pLayerCfg.WindowY1 = LCD_HEIGHT;
    pLayerCfg.PixelFormat = LTDC_PIXEL_FORMAT_RGB565;
    pLayerCfg.Alpha = 255;  // Pełna nieprzezroczystość
    pLayerCfg.Alpha0 = 0;
    pLayerCfg.BlendingFactor1 = LTDC_BLENDING_FACTOR1_CA;
    pLayerCfg.BlendingFactor2 = LTDC_BLENDING_FACTOR2_CA;
    pLayerCfg.FBStartAdress = (uint32_t)framebuffer;
    pLayerCfg.ImageWidth = LCD_WIDTH;
    pLayerCfg.ImageHeight = LCD_HEIGHT;
    pLayerCfg.Backcolor.Blue = 0;
    pLayerCfg.Backcolor.Green = 0;
    pLayerCfg.Backcolor.Red = 0;
    
    if (HAL_LTDC_ConfigLayer(&hltdc, &pLayerCfg, 0) != HAL_OK) {
        Error_Handler();
    }
}
```

## 🎨 Podstawowe funkcje rysowania

### Konwersja kolorów RGB565

```c
/**
 * @brief  Konwersja RGB888 do RGB565
 */
uint16_t RGB888_to_RGB565(uint8_t r, uint8_t g, uint8_t b)
{
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3);
}

/**
 * @brief  Predefiniowane kolory RGB565
 */
#define COLOR_BLACK   0x0000
#define COLOR_WHITE   0xFFFF
#define COLOR_RED     0xF800
#define COLOR_GREEN   0x07E0
#define COLOR_BLUE    0x001F
#define COLOR_YELLOW  0xFFE0
#define COLOR_CYAN    0x07FF
#define COLOR_MAGENTA 0xF81F
```

### Rysowanie piksela i linii

```c
/**
 * @brief  Ustaw kolor piksela
 */
void LCD_DrawPixel(uint16_t x, uint16_t y, uint16_t color)
{
    if (x < LCD_WIDTH && y < LCD_HEIGHT) {
        framebuffer[y * LCD_WIDTH + x] = color;
    }
}

/**
 * @brief  Wypełnij ekran kolorem
 */
void LCD_Clear(uint16_t color)
{
    for (uint32_t i = 0; i < LCD_WIDTH * LCD_HEIGHT; i++) {
        framebuffer[i] = color;
    }
}

/**
 * @brief  Narysuj prostokąt
 */
void LCD_FillRect(uint16_t x, uint16_t y, uint16_t width, uint16_t height, uint16_t color)
{
    for (uint16_t i = 0; i < height; i++) {
        for (uint16_t j = 0; j < width; j++) {
            LCD_DrawPixel(x + j, y + i, color);
        }
    }
}

/**
 * @brief  Narysuj linię (algorytm Bresenhama)
 */
void LCD_DrawLine(int16_t x0, int16_t y0, int16_t x1, int16_t y1, uint16_t color)
{
    int16_t dx = abs(x1 - x0);
    int16_t dy = abs(y1 - y0);
    int16_t sx = (x0 < x1) ? 1 : -1;
    int16_t sy = (y0 < y1) ? 1 : -1;
    int16_t err = dx - dy;
    
    while (1) {
        LCD_DrawPixel(x0, y0, color);
        
        if (x0 == x1 && y0 == y1) break;
        
        int16_t e2 = 2 * err;
        if (e2 > -dy) {
            err -= dy;
            x0 += sx;
        }
        if (e2 < dx) {
            err += dx;
            y0 += sy;
        }
    }
}

/**
 * @brief  Narysuj okrąg
 */
void LCD_DrawCircle(int16_t x0, int16_t y0, int16_t radius, uint16_t color)
{
    int16_t x = radius;
    int16_t y = 0;
    int16_t err = 0;
    
    while (x >= y) {
        LCD_DrawPixel(x0 + x, y0 + y, color);
        LCD_DrawPixel(x0 + y, y0 + x, color);
        LCD_DrawPixel(x0 - y, y0 + x, color);
        LCD_DrawPixel(x0 - x, y0 + y, color);
        LCD_DrawPixel(x0 - x, y0 - y, color);
        LCD_DrawPixel(x0 - y, y0 - x, color);
        LCD_DrawPixel(x0 + y, y0 - x, color);
        LCD_DrawPixel(x0 + x, y0 - y, color);
        
        if (err <= 0) {
            y++;
            err += 2*y + 1;
        }
        if (err > 0) {
            x--;
            err -= 2*x + 1;
        }
    }
}
```

## 🔤 Wyświetlanie tekstu

### Prosty font 8x8

```c
/**
 * @brief  Font 8x8 (ASCII)
 */
extern const uint8_t font8x8[128][8];  // Tablica znaków

/**
 * @brief  Wyświetl znak
 */
void LCD_DrawChar(uint16_t x, uint16_t y, char c, uint16_t fg_color, uint16_t bg_color)
{
    for (uint8_t i = 0; i < 8; i++) {
        uint8_t line = font8x8[(uint8_t)c][i];
        
        for (uint8_t j = 0; j < 8; j++) {
            if (line & (1 << j)) {
                LCD_DrawPixel(x + j, y + i, fg_color);
            } else {
                LCD_DrawPixel(x + j, y + i, bg_color);
            }
        }
    }
}

/**
 * @brief  Wyświetl string
 */
void LCD_DrawString(uint16_t x, uint16_t y, const char *str, uint16_t fg_color, uint16_t bg_color)
{
    uint16_t pos_x = x;
    
    while (*str) {
        if (*str == '\n') {
            pos_x = x;
            y += 8;
        } else {
            LCD_DrawChar(pos_x, y, *str, fg_color, bg_color);
            pos_x += 8;
        }
        str++;
    }
}

/**
 * @brief  Wyświetl liczbę
 */
void LCD_DrawNumber(uint16_t x, uint16_t y, int32_t number, uint16_t fg_color, uint16_t bg_color)
{
    char buffer[12];
    sprintf(buffer, "%ld", number);
    LCD_DrawString(x, y, buffer, fg_color, bg_color);
}
```

## 🖼️ DMA2D - Akcelerator graficzny

### Szybkie kopiowanie i wypełnianie

```c
/**
 * @brief  Konfiguracja DMA2D
 */
DMA2D_HandleTypeDef hdma2d;

void DMA2D_Init(void)
{
    __HAL_RCC_DMA2D_CLK_ENABLE();
    
    hdma2d.Instance = DMA2D;
    hdma2d.Init.Mode = DMA2D_M2M;  // Memory to Memory
    hdma2d.Init.ColorMode = DMA2D_OUTPUT_RGB565;
    hdma2d.Init.OutputOffset = 0;
    
    HAL_DMA2D_Init(&hdma2d);
}

/**
 * @brief  Szybkie wypełnienie prostokąta (DMA2D)
 */
void DMA2D_FillRect(uint16_t x, uint16_t y, uint16_t width, uint16_t height, uint16_t color)
{
    uint32_t destination = (uint32_t)&framebuffer[y * LCD_WIDTH + x];
    
    hdma2d.Init.Mode = DMA2D_R2M;  // Register to Memory
    hdma2d.Init.ColorMode = DMA2D_OUTPUT_RGB565;
    hdma2d.Init.OutputOffset = LCD_WIDTH - width;
    
    HAL_DMA2D_Init(&hdma2d);
    HAL_DMA2D_Start(&hdma2d, color, destination, width, height);
    HAL_DMA2D_PollForTransfer(&hdma2d, 100);
}

/**
 * @brief  Kopiowanie obrazu (DMA2D)
 */
void DMA2D_CopyImage(uint16_t *src, uint16_t x, uint16_t y, uint16_t width, uint16_t height)
{
    uint32_t source = (uint32_t)src;
    uint32_t destination = (uint32_t)&framebuffer[y * LCD_WIDTH + x];
    
    hdma2d.Init.Mode = DMA2D_M2M;
    hdma2d.Init.ColorMode = DMA2D_OUTPUT_RGB565;
    hdma2d.Init.OutputOffset = LCD_WIDTH - width;
    
    hdma2d.LayerCfg[1].InputOffset = 0;
    hdma2d.LayerCfg[1].InputColorMode = DMA2D_INPUT_RGB565;
    hdma2d.LayerCfg[1].AlphaMode = DMA2D_NO_MODIF_ALPHA;
    hdma2d.LayerCfg[1].InputAlpha = 0xFF;
    
    HAL_DMA2D_Init(&hdma2d);
    HAL_DMA2D_ConfigLayer(&hdma2d, 1);
    HAL_DMA2D_Start(&hdma2d, source, destination, width, height);
    HAL_DMA2D_PollForTransfer(&hdma2d, 100);
}
```

## 🎭 Double Buffering

### Eliminacja migotania

```c
/**
 * @brief  Double buffer configuration
 */
__attribute__((section(".sdram"))) uint16_t framebuffer0[LCD_WIDTH * LCD_HEIGHT];
__attribute__((section(".sdram"))) uint16_t framebuffer1[LCD_WIDTH * LCD_HEIGHT];

uint16_t *active_buffer = framebuffer0;
uint16_t *draw_buffer = framebuffer1;

/**
 * @brief  Zamiana buforów
 */
void LCD_SwapBuffers(void)
{
    // Czekaj na VBlank
    while (!(LTDC->CDSR & LTDC_CDSR_VSYNCS));
    
    // Zamień wskaźniki
    uint16_t *temp = active_buffer;
    active_buffer = draw_buffer;
    draw_buffer = temp;
    
    // Ustaw nowy adres framebuffera
    LTDC_Layer1->CFBAR = (uint32_t)active_buffer;
    
    // Przeładuj konfigurację
    LTDC->SRCR = LTDC_SRCR_VBR;  // Vertical Blanking Reload
}

/**
 * @brief  Przykład użycia
 */
void Animation_Loop(void)
{
    while (1) {
        // Rysuj do draw_buffer
        LCD_Clear_Buffer(draw_buffer, COLOR_BLACK);
        LCD_DrawCircle_Buffer(draw_buffer, 240, 136, 50, COLOR_RED);
        
        // Zamień bufory
        LCD_SwapBuffers();
        
        HAL_Delay(16);  // ~60 FPS
    }
}
```

## 📊 Przykładowe aplikacje graficzne

### Prosty dashboard

```c
/**
 * @brief  Wyświetl dashboard z danymi
 */
void Display_Dashboard(float temperature, float humidity, uint32_t uptime)
{
    char buffer[32];
    
    // Tło
    LCD_Clear(COLOR_BLACK);
    
    // Nagłówek
    LCD_FillRect(0, 0, LCD_WIDTH, 30, COLOR_BLUE);
    LCD_DrawString(10, 10, "STM32F429 Dashboard", COLOR_WHITE, COLOR_BLUE);
    
    // Temperatura
    LCD_DrawString(10, 50, "Temperature:", COLOR_WHITE, COLOR_BLACK);
    sprintf(buffer, "%.1f C", temperature);
    LCD_DrawString(150, 50, buffer, COLOR_YELLOW, COLOR_BLACK);
    
    // Wilgotność
    LCD_DrawString(10, 80, "Humidity:", COLOR_WHITE, COLOR_BLACK);
    sprintf(buffer, "%.1f %%", humidity);
    LCD_DrawString(150, 80, buffer, COLOR_CYAN, COLOR_BLACK);
    
    // Uptime
    LCD_DrawString(10, 110, "Uptime:", COLOR_WHITE, COLOR_BLACK);
    sprintf(buffer, "%lu s", uptime);
    LCD_DrawString(150, 110, buffer, COLOR_GREEN, COLOR_BLACK);
    
    // Pasek postępu
    uint16_t bar_width = (uint16_t)((temperature / 50.0f) * 400);
    LCD_FillRect(40, 150, bar_width, 20, COLOR_RED);
    LCD_DrawRect(40, 150, 400, 20, COLOR_WHITE);
}
```

## 🔗 Powiązane tematy

- [[stm32f429i_dma|STM32F429I - DMA]]
- [[stm32f429i_spi|STM32F429I - SPI]]
- [[stm32f429i_fmc|STM32F429I - FMC i pamięci zewnętrzne]]

## 📝 Wzory i obliczenia

### Timing calculation
```
Pixel Clock = (HDISP + HFP + HSYNC + HBP) × 
              (VDISP + VFP + VSYNC + VBP) × 
              Refresh Rate

Dla 480x272 @ 60 Hz:
Pixel Clock ≈ 9 MHz
```

### Rozmiar framebuffera
```
RGB565: Width × Height × 2 bytes
RGB888: Width × Height × 3 bytes
ARGB8888: Width × Height × 4 bytes

480×272 RGB565 = 261,120 bytes ≈ 255 KB
```

---

*Powiązane notatki: [[embedded_systems_index|Systemy Wbudowane - Kompendium]]*
