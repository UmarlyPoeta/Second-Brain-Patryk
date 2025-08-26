# 🏗️ Maven - Build Tool

## 📚 Wprowadzenie
Apache Maven to narzędzie do automatyzacji budowania projektów Java, zarządzania zależnościami i lifecycle'em projektów. Używa deklaratywnego podejścia z plikiem POM (Project Object Model) do konfiguracji projektu.

## 🎯 Struktura Projektu Maven

### Standard Directory Layout
```
my-app/
├── pom.xml                          # Project Object Model
├── src/
│   ├── main/
│   │   ├── java/                    # Production Java code
│   │   │   └── com/example/app/
│   │   │       └── App.java
│   │   ├── resources/               # Production resources
│   │   │   ├── application.properties
│   │   │   ├── logback.xml
│   │   │   └── static/
│   │   └── webapp/                  # Web application files (for web projects)
│   │       ├── WEB-INF/
│   │       │   └── web.xml
│   │       └── index.html
│   └── test/
│       ├── java/                    # Test Java code
│       │   └── com/example/app/
│       │       └── AppTest.java
│       └── resources/               # Test resources
│           └── test.properties
├── target/                          # Build output (generated)
│   ├── classes/
│   ├── test-classes/
│   └── my-app-1.0.jar
└── README.md
```

## 📋 POM.xml - Project Object Model

### Podstawowy POM
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- Project coordinates -->
    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <!-- Project information -->
    <name>My Application</name>
    <description>A sample Java application built with Maven</description>
    <url>https://github.com/example/my-app</url>

    <!-- Properties for version management -->
    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        <project.reporting.outputEncoding>UTF-8</project.reporting.outputEncoding>
        
        <!-- Dependency versions -->
        <junit.version>5.10.0</junit.version>
        <mockito.version>5.5.0</mockito.version>
        <jackson.version>2.15.2</jackson.version>
        <slf4j.version>2.0.9</slf4j.version>
        <logback.version>1.4.11</logback.version>
    </properties>

    <!-- Dependencies -->
    <dependencies>
        <!-- Compile dependencies -->
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>${jackson.version}</version>
        </dependency>

        <dependency>
            <groupId>org.slf4j</groupId>
            <artifactId>slf4j-api</artifactId>
            <version>${slf4j.version}</version>
        </dependency>

        <dependency>
            <groupId>ch.qos.logback</groupId>
            <artifactId>logback-classic</artifactId>
            <version>${logback.version}</version>
        </dependency>

        <!-- Test dependencies -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${junit.version}</version>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-core</artifactId>
            <version>${mockito.version}</version>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-junit-jupiter</artifactId>
            <version>${mockito.version}</version>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <!-- Build configuration -->
    <build>
        <finalName>${project.artifactId}-${project.version}</finalName>
        
        <plugins>
            <!-- Compiler plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>${maven.compiler.source}</source>
                    <target>${maven.compiler.target}</target>
                    <encoding>${project.build.sourceEncoding}</encoding>
                </configuration>
            </plugin>

            <!-- Surefire plugin for running tests -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.1</version>
                <configuration>
                    <includes>
                        <include>**/*Test.java</include>
                        <include>**/*Tests.java</include>
                    </includes>
                </configuration>
            </plugin>
        </plugins>
    </build>
</project>
```

### Zaawansowany POM z Profilami
```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>enterprise-app</artifactId>
    <version>2.1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <name>Enterprise Application</name>
    <description>A comprehensive enterprise Java application</description>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        
        <!-- Spring Boot version -->
        <spring-boot.version>3.1.5</spring-boot.version>
        
        <!-- Database -->
        <postgresql.version>42.6.0</postgresql.version>
        <h2.version>2.2.224</h2.version>
        
        <!-- Testing -->
        <testcontainers.version>1.19.1</testcontainers.version>
        
        <!-- Plugin versions -->
        <jacoco.version>0.8.10</jacoco.version>
        <spotbugs.version>4.7.3.6</spotbugs.version>
    </properties>

    <!-- Dependency Management -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            
            <dependency>
                <groupId>org.testcontainers</groupId>
                <artifactId>testcontainers-bom</artifactId>
                <version>${testcontainers.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <dependencies>
        <!-- Spring Boot starters -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- Database -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <version>${postgresql.version}</version>
            <scope>runtime</scope>
        </dependency>

        <!-- Test dependencies -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>postgresql</artifactId>
            <scope>test</scope>
        </dependency>
        
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <!-- Build configuration -->
    <build>
        <finalName>${project.artifactId}</finalName>
        
        <plugins>
            <!-- Spring Boot plugin -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <version>${spring-boot.version}</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>repackage</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>

            <!-- Compiler plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>${maven.compiler.source}</source>
                    <target>${maven.compiler.target}</target>
                    <encoding>${project.build.sourceEncoding}</encoding>
                    <compilerArgs>
                        <arg>-parameters</arg>
                    </compilerArgs>
                </configuration>
            </plugin>

            <!-- Test plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.2.1</version>
                <configuration>
                    <includes>
                        <include>**/*Test.java</include>
                        <include>**/*Tests.java</include>
                    </includes>
                    <excludes>
                        <exclude>**/*IntegrationTest.java</exclude>
                    </excludes>
                </configuration>
            </plugin>

            <!-- Integration test plugin -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-failsafe-plugin</artifactId>
                <version>3.2.1</version>
                <configuration>
                    <includes>
                        <include>**/*IntegrationTest.java</include>
                        <include>**/*IT.java</include>
                    </includes>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>integration-test</goal>
                            <goal>verify</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>

            <!-- Code coverage with JaCoCo -->
            <plugin>
                <groupId>org.jacoco</groupId>
                <artifactId>jacoco-maven-plugin</artifactId>
                <version>${jacoco.version}</version>
                <executions>
                    <execution>
                        <goals>
                            <goal>prepare-agent</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>report</id>
                        <phase>test</phase>
                        <goals>
                            <goal>report</goal>
                        </goals>
                    </execution>
                    <execution>
                        <id>check</id>
                        <goals>
                            <goal>check</goal>
                        </goals>
                        <configuration>
                            <rules>
                                <rule>
                                    <element>BUNDLE</element>
                                    <limits>
                                        <limit>
                                            <counter>INSTRUCTION</counter>
                                            <value>COVEREDRATIO</value>
                                            <minimum>0.80</minimum>
                                        </limit>
                                    </limits>
                                </rule>
                            </rules>
                        </configuration>
                    </execution>
                </executions>
            </plugin>

            <!-- Static analysis with SpotBugs -->
            <plugin>
                <groupId>com.github.spotbugs</groupId>
                <artifactId>spotbugs-maven-plugin</artifactId>
                <version>${spotbugs.version}</version>
                <configuration>
                    <effort>Max</effort>
                    <threshold>Medium</threshold>
                </configuration>
                <executions>
                    <execution>
                        <goals>
                            <goal>check</goal>
                        </goals>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>

    <!-- Profiles for different environments -->
    <profiles>
        <profile>
            <id>development</id>
            <activation>
                <activeByDefault>true</activeByDefault>
            </activation>
            <dependencies>
                <dependency>
                    <groupId>com.h2database</groupId>
                    <artifactId>h2</artifactId>
                    <version>${h2.version}</version>
                    <scope>runtime</scope>
                </dependency>
                
                <dependency>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-devtools</artifactId>
                    <scope>runtime</scope>
                    <optional>true</optional>
                </dependency>
            </dependencies>
        </profile>

        <profile>
            <id>production</id>
            <build>
                <plugins>
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-source-plugin</artifactId>
                        <version>3.3.0</version>
                        <executions>
                            <execution>
                                <id>attach-sources</id>
                                <goals>
                                    <goal>jar</goal>
                                </goals>
                            </execution>
                        </executions>
                    </plugin>
                    
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-javadoc-plugin</artifactId>
                        <version>3.6.0</version>
                        <executions>
                            <execution>
                                <id>attach-javadocs</id>
                                <goals>
                                    <goal>jar</goal>
                                </goals>
                            </execution>
                        </executions>
                    </plugin>
                </plugins>
            </build>
        </profile>

        <profile>
            <id>docker</id>
            <build>
                <plugins>
                    <plugin>
                        <groupId>com.spotify</groupId>
                        <artifactId>dockerfile-maven-plugin</artifactId>
                        <version>1.4.13</version>
                        <configuration>
                            <repository>${project.artifactId}</repository>
                            <tag>${project.version}</tag>
                            <buildArgs>
                                <JAR_FILE>target/${project.build.finalName}.jar</JAR_FILE>
                            </buildArgs>
                        </configuration>
                        <executions>
                            <execution>
                                <id>default</id>
                                <goals>
                                    <goal>build</goal>
                                    <goal>push</goal>
                                </goals>
                            </execution>
                        </executions>
                    </plugin>
                </plugins>
            </build>
        </profile>
    </profiles>
</project>
```

## 📦 Zarządzanie Zależnościami

### Scopes Dependencies
```xml
<dependencies>
    <!-- COMPILE (default) - available in all phases -->
    <dependency>
        <groupId>org.springframework</groupId>
        <artifactId>spring-core</artifactId>
        <version>6.0.12</version>
        <!-- scope>compile</scope --> <!-- default -->
    </dependency>

    <!-- PROVIDED - available at compile time, not packaged -->
    <dependency>
        <groupId>javax.servlet</groupId>
        <artifactId>servlet-api</artifactId>
        <version>2.5</version>
        <scope>provided</scope>
    </dependency>

    <!-- RUNTIME - not needed for compilation, only for runtime -->
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <version>8.0.33</version>
        <scope>runtime</scope>
    </dependency>

    <!-- TEST - only available for test compilation and execution -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>

    <!-- SYSTEM - similar to provided, but JAR location explicitly specified -->
    <dependency>
        <groupId>com.sun</groupId>
        <artifactId>tools</artifactId>
        <version>1.8</version>
        <scope>system</scope>
        <systemPath>${java.home}/../lib/tools.jar</systemPath>
    </dependency>

    <!-- IMPORT - only used in dependencyManagement section -->
    <!-- See dependencyManagement example above -->
</dependencies>
```

### Dependency Management i BOM (Bill of Materials)
```xml
<!-- Parent POM or in dependencyManagement section -->
<dependencyManagement>
    <dependencies>
        <!-- Spring Boot BOM -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-dependencies</artifactId>
            <version>3.1.5</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        
        <!-- Jackson BOM -->
        <dependency>
            <groupId>com.fasterxml.jackson</groupId>
            <artifactId>jackson-bom</artifactId>
            <version>2.15.2</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
        
        <!-- Custom version management -->
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-lang3</artifactId>
            <version>3.13.0</version>
        </dependency>
        
        <dependency>
            <groupId>commons-io</groupId>
            <artifactId>commons-io</artifactId>
            <version>2.13.0</version>
        </dependency>
    </dependencies>
</dependencyManagement>

<!-- Later in dependencies section - no version needed -->
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <!-- version managed by BOM -->
    </dependency>
    
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <!-- version managed by BOM -->
    </dependency>
    
    <dependency>
        <groupId>org.apache.commons</groupId>
        <artifactId>commons-lang3</artifactId>
        <!-- version managed by dependencyManagement -->
    </dependency>
</dependencies>
```

### Excludes i Optional Dependencies
```xml
<dependencies>
    <!-- Excluding transitive dependencies -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
        <exclusions>
            <exclusion>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-starter-tomcat</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
    
    <!-- Use Jetty instead of Tomcat -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jetty</artifactId>
    </dependency>
    
    <!-- Optional dependency - not transitively included -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-devtools</artifactId>
        <scope>runtime</scope>
        <optional>true</optional>
    </dependency>
    
    <!-- Exclude specific transitive dependency -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-logging</artifactId>
        <exclusions>
            <exclusion>
                <groupId>ch.qos.logback</groupId>
                <artifactId>logback-classic</artifactId>
            </exclusion>
        </exclusions>
    </dependency>
    
    <!-- Use Log4j2 instead -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-log4j2</artifactId>
    </dependency>
</dependencies>
```

## 🔄 Maven Lifecycle i Phases

### Lifecycle Phases
```bash
# Default Lifecycle
mvn validate       # validate project is correct and all necessary information is available
mvn compile        # compile source code of the project
mvn test           # test compiled source code using a unit testing framework
mvn package        # take compiled code and package it (e.g., JAR)
mvn verify         # run any checks to verify the package is valid
mvn install        # install package into local repository
mvn deploy         # copy final package to remote repository

# Clean Lifecycle
mvn clean          # clean up artifacts created by build

# Site Lifecycle
mvn site           # create site documentation

# Combined commands
mvn clean compile           # Clean then compile
mvn clean test             # Clean, compile, and test
mvn clean package          # Clean, compile, test, and package
mvn clean install          # Clean, compile, test, package, and install
mvn clean deploy           # Full lifecycle including deploy
```

### Custom Lifecycle Configuration
```xml
<build>
    <plugins>
        <!-- Custom plugin execution -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-antrun-plugin</artifactId>
            <version>3.1.0</version>
            <executions>
                <execution>
                    <id>pre-compile-tasks</id>
                    <phase>generate-sources</phase>
                    <goals>
                        <goal>run</goal>
                    </goals>
                    <configuration>
                        <target>
                            <echo message="Generating sources..." />
                            <mkdir dir="${project.build.directory}/generated-sources" />
                        </target>
                    </configuration>
                </execution>
                
                <execution>
                    <id>post-compile-tasks</id>
                    <phase>process-classes</phase>
                    <goals>
                        <goal>run</goal>
                    </goals>
                    <configuration>
                        <target>
                            <echo message="Post-processing compiled classes..." />
                        </target>
                    </configuration>
                </execution>
            </executions>
        </plugin>
        
        <!-- Copy resources during build -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-resources-plugin</artifactId>
            <version>3.3.1</version>
            <executions>
                <execution>
                    <id>copy-resources</id>
                    <phase>process-resources</phase>
                    <goals>
                        <goal>copy-resources</goal>
                    </goals>
                    <configuration>
                        <outputDirectory>${project.build.directory}/extra-resources</outputDirectory>
                        <resources>
                            <resource>
                                <directory>src/main/config</directory>
                                <filtering>true</filtering>
                            </resource>
                        </resources>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

## 🔌 Popularne Pluginy

### Essential Plugins
```xml
<build>
    <plugins>
        <!-- Compiler Plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.11.0</version>
            <configuration>
                <source>17</source>
                <target>17</target>
                <encoding>UTF-8</encoding>
                <showWarnings>true</showWarnings>
                <showDeprecation>true</showDeprecation>
                <compilerArgs>
                    <arg>-Xlint:all</arg>
                    <arg>-parameters</arg>
                </compilerArgs>
            </configuration>
        </plugin>

        <!-- JAR Plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-jar-plugin</artifactId>
            <version>3.3.0</version>
            <configuration>
                <archive>
                    <manifest>
                        <addClasspath>true</addClasspath>
                        <classpathPrefix>lib/</classpathPrefix>
                        <mainClass>com.example.Main</mainClass>
                        <addDefaultImplementationEntries>true</addDefaultImplementationEntries>
                        <addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
                    </manifest>
                    <manifestEntries>
                        <Built-By>${user.name}</Built-By>
                        <Build-Time>${maven.build.timestamp}</Build-Time>
                        <Build-Version>${project.version}</Build-Version>
                    </manifestEntries>
                </archive>
            </configuration>
        </plugin>

        <!-- Assembly Plugin - create distribution packages -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-assembly-plugin</artifactId>
            <version>3.6.0</version>
            <configuration>
                <descriptorRefs>
                    <descriptorRef>jar-with-dependencies</descriptorRef>
                </descriptorRefs>
                <archive>
                    <manifest>
                        <mainClass>com.example.Main</mainClass>
                    </manifest>
                </archive>
            </configuration>
            <executions>
                <execution>
                    <id>make-assembly</id>
                    <phase>package</phase>
                    <goals>
                        <goal>single</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>

        <!-- Shade Plugin - create uber jar -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-shade-plugin</artifactId>
            <version>3.5.1</version>
            <configuration>
                <createDependencyReducedPom>false</createDependencyReducedPom>
                <filters>
                    <filter>
                        <artifact>*:*</artifact>
                        <excludes>
                            <exclude>META-INF/*.SF</exclude>
                            <exclude>META-INF/*.DSA</exclude>
                            <exclude>META-INF/*.RSA</exclude>
                        </excludes>
                    </filter>
                </filters>
            </configuration>
            <executions>
                <execution>
                    <phase>package</phase>
                    <goals>
                        <goal>shade</goal>
                    </goals>
                    <configuration>
                        <transformers>
                            <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                <mainClass>com.example.Main</mainClass>
                            </transformer>
                        </transformers>
                    </configuration>
                </execution>
            </executions>
        </plugin>

        <!-- Dependency Plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-dependency-plugin</artifactId>
            <version>3.6.1</version>
            <executions>
                <execution>
                    <id>copy-dependencies</id>
                    <phase>prepare-package</phase>
                    <goals>
                        <goal>copy-dependencies</goal>
                    </goals>
                    <configuration>
                        <outputDirectory>${project.build.directory}/lib</outputDirectory>
                        <overWriteReleases>false</overWriteReleases>
                        <overWriteSnapshots>false</overWriteSnapshots>
                        <overWriteIfNewer>true</overWriteIfNewer>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

### Code Quality Plugins
```xml
<build>
    <plugins>
        <!-- Checkstyle Plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-checkstyle-plugin</artifactId>
            <version>3.3.1</version>
            <configuration>
                <configLocation>checkstyle.xml</configLocation>
                <encoding>UTF-8</encoding>
                <consoleOutput>true</consoleOutput>
                <failsOnError>true</failsOnError>
                <includeTestSourceDirectory>true</includeTestSourceDirectory>
            </configuration>
            <executions>
                <execution>
                    <id>validate</id>
                    <phase>validate</phase>
                    <goals>
                        <goal>check</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>

        <!-- PMD Plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-pmd-plugin</artifactId>
            <version>3.21.2</version>
            <configuration>
                <rulesets>
                    <ruleset>/category/java/bestpractices.xml</ruleset>
                    <ruleset>/category/java/codestyle.xml</ruleset>
                    <ruleset>/category/java/design.xml</ruleset>
                    <ruleset>/category/java/errorprone.xml</ruleset>
                    <ruleset>/category/java/performance.xml</ruleset>
                    <ruleset>/category/java/security.xml</ruleset>
                </rulesets>
                <printFailingErrors>true</printFailingErrors>
            </configuration>
            <executions>
                <execution>
                    <goals>
                        <goal>check</goal>
                    </goals>
                </execution>
            </executions>
        </plugin>

        <!-- Versions Plugin -->
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>versions-maven-plugin</artifactId>
            <version>2.16.1</version>
            <configuration>
                <generateBackupPoms>false</generateBackupPoms>
            </configuration>
        </plugin>
    </plugins>
</build>
```

## 🎛️ Maven Properties i Filtering

### Properties Definition i Usage
```xml
<properties>
    <!-- Built-in properties -->
    <!-- ${project.groupId}, ${project.artifactId}, ${project.version} -->
    <!-- ${project.build.directory}, ${project.build.outputDirectory} -->
    <!-- ${maven.build.timestamp} -->
    
    <!-- Custom properties -->
    <app.name>My Application</app.name>
    <app.version>${project.version}</app.version>
    <build.timestamp>${maven.build.timestamp}</build.timestamp>
    <maven.build.timestamp.format>yyyy-MM-dd HH:mm:ss</maven.build.timestamp.format>
    
    <!-- Environment-specific properties -->
    <database.driver>org.h2.Driver</database.driver>
    <database.url>jdbc:h2:mem:testdb</database.url>
    <database.username>sa</database.username>
    <database.password></database.password>
    
    <!-- Plugin versions -->
    <maven-compiler-plugin.version>3.11.0</maven-compiler-plugin.version>
    <maven-surefire-plugin.version>3.2.1</maven-surefire-plugin.version>
</properties>

<!-- Resource filtering -->
<build>
    <resources>
        <resource>
            <directory>src/main/resources</directory>
            <filtering>true</filtering>
            <includes>
                <include>**/*.properties</include>
                <include>**/*.xml</include>
                <include>**/*.yml</include>
            </includes>
        </resource>
        <resource>
            <directory>src/main/resources</directory>
            <filtering>false</filtering>
            <excludes>
                <exclude>**/*.properties</exclude>
                <exclude>**/*.xml</exclude>
                <exclude>**/*.yml</exclude>
            </excludes>
        </resource>
    </resources>
</build>
```

### application.properties with filtering
```properties
# src/main/resources/application.properties
app.name=${app.name}
app.version=${app.version}
build.timestamp=${build.timestamp}

# Database configuration
database.driver=${database.driver}
database.url=${database.url}
database.username=${database.username}
database.password=${database.password}

# Environment
environment=${environment}
debug.enabled=${debug.enabled}
```

## 🎯 Multi-module Projects

### Parent POM
```xml
<!-- parent-project/pom.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>parent-project</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>pom</packaging>

    <name>Parent Project</name>
    <description>Multi-module parent project</description>

    <!-- Modules -->
    <modules>
        <module>common</module>
        <module>domain</module>
        <module>service</module>
        <module>web</module>
        <module>integration-tests</module>
    </modules>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
        
        <spring-boot.version>3.1.5</spring-boot.version>
        <junit.version>5.10.0</junit.version>
    </properties>

    <!-- Dependency Management for all modules -->
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-dependencies</artifactId>
                <version>${spring-boot.version}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
            
            <!-- Inter-module dependencies -->
            <dependency>
                <groupId>${project.groupId}</groupId>
                <artifactId>common</artifactId>
                <version>${project.version}</version>
            </dependency>
            
            <dependency>
                <groupId>${project.groupId}</groupId>
                <artifactId>domain</artifactId>
                <version>${project.version}</version>
            </dependency>
            
            <dependency>
                <groupId>${project.groupId}</groupId>
                <artifactId>service</artifactId>
                <version>${project.version}</version>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <!-- Plugin Management for all modules -->
    <build>
        <pluginManagement>
            <plugins>
                <plugin>
                    <groupId>org.apache.maven.plugins</groupId>
                    <artifactId>maven-compiler-plugin</artifactId>
                    <version>3.11.0</version>
                    <configuration>
                        <source>${maven.compiler.source}</source>
                        <target>${maven.compiler.target}</target>
                        <encoding>${project.build.sourceEncoding}</encoding>
                    </configuration>
                </plugin>
                
                <plugin>
                    <groupId>org.springframework.boot</groupId>
                    <artifactId>spring-boot-maven-plugin</artifactId>
                    <version>${spring-boot.version}</version>
                </plugin>
            </plugins>
        </pluginManagement>
    </build>
</project>
```

### Child Module POM
```xml
<!-- common/pom.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.example</groupId>
        <artifactId>parent-project</artifactId>
        <version>1.0.0-SNAPSHOT</version>
    </parent>

    <artifactId>common</artifactId>
    <packaging>jar</packaging>

    <name>Common Module</name>
    <description>Common utilities and shared code</description>

    <dependencies>
        <!-- Dependencies specific to this module -->
        <dependency>
            <groupId>org.apache.commons</groupId>
            <artifactId>commons-lang3</artifactId>
        </dependency>
        
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
        </dependency>

        <!-- Test dependencies -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>
</project>
```

## 🔗 Powiązane Tematy
- [[Gradle - Alternatywa dla Maven]] - Moderne build tool
- [[Spring Boot Wprowadzenie]] - Spring Boot z Maven
- [[CI/CD dla Java Applications]] - Maven w pipeline'ach
- [[Docker - Konteneryzacja Java Apps]] - Containerizing Maven projects

## 💡 Najlepsze Praktyki

1. **Używaj dependency management** do zarządzania wersjami
2. **Definiuj wersje w properties** - łatwiejsze aktualizacje
3. **Używaj BOM imports** dla spójnych wersji
4. **Grupuj pluginy w pluginManagement** w parent POM
5. **Separuj test dependencies** odpowiednimi scopes
6. **Używaj profiles** dla różnych środowisk
7. **Regularnie aktualizuj dependencies** i pluginy
8. **Dokumentuj custom configuration** w README

## ⚠️ Częste Problemy

1. **Dependency conflicts** - użyj `mvn dependency:tree` do diagnozy
2. **Snapshot dependencies** w produkcji - unikaj ich
3. **Classpath issues** - sprawdź scopes dependencies
4. **Plugin version conflicts** - definiuj wersje explicitly
5. **Out of memory** podczas build - zwiększ MAVEN_OPTS

## 🛠️ Przydatne Komendy

```bash
# Diagnostyka
mvn dependency:tree                    # Pokaż drzewo zależności
mvn dependency:analyze                 # Analizuj nieużywane zależności
mvn versions:display-dependency-updates # Sprawdź dostępne aktualizacje
mvn help:effective-pom                 # Pokaż efektywny POM

# Development
mvn clean compile                      # Czysta kompilacja
mvn clean test                         # Testy jednostkowe
mvn clean package -DskipTests         # Package bez testów
mvn clean install -Pproduction        # Install z profilem production

# Debugging
mvn -X clean compile                   # Debug mode (verbose)
mvn -o clean package                   # Offline mode
mvn clean compile -Dmaven.compiler.verbose=true  # Verbose compilation
```

---
*Czas nauki: ~30 minut | Poziom: Średniozaawansowany*