# 📊 Spring Boot Actuator - Monitoring i Observability

## 📋 Wprowadzenie do Production-Ready Features

Spring Boot Actuator to kluczowy moduł, który przekształca aplikacje Spring Boot w production-ready systems poprzez dodanie comprehensive monitoring, health checking, i operational endpoints. W środowiskach enterprise, gdzie applications muszą być monitored 24/7, Actuator dostarcza essential insights do application health, performance metrics, i operational status, umożliwiając proactive maintenance i rapid troubleshooting.

### Teoria Observability

**Observability vs Monitoring:**
Observability to szersze pojęcie niż monitoring - to ability to understand internal state of systemu based na jego external outputs.

**Three Pillars of Observability:**

**Metrics (Metryki):**
Numerical measurements over time intervals:
- Counter metrics (monotonically increasing)
- Gauge metrics (point-in-time values)
- Timer metrics (duration measurements)
- Distribution summaries (statistical distributions)

**Logs (Logi):**
Structured lub unstructured event records:
- Application logs (business events)
- Access logs (request/response records)  
- Error logs (exception traces)
- Audit logs (security events)

**Traces (Ślady):**
Request flow through distributed system:
- Distributed tracing across microservices
- Performance bottleneck identification
- Dependency relationship mapping
- Error propagation analysis

### DevOps Integration

**Site Reliability Engineering (SRE) Principles:**
- **Error budgets:** Acceptable failure rate
- **Service Level Indicators (SLI):** Measurable aspects of service level
- **Service Level Objectives (SLO):** Target values dla SLIs
- **Service Level Agreements (SLA):** Business contracts based on SLOs

**Continuous Monitoring:**
- Real-time alerting na critical metrics
- Automated response to common issues
- Capacity planning based na trends
- Performance regression detection

## 🔧 Actuator Endpoints Deep Dive

### Health Indicators

**Health Check Theory:**
Health checks to fundamental building blocks of service reliability, providing automated way to determine czy service is functioning properly i ready to serve traffic.

**Built-in Health Indicators:**
- **DiskSpaceHealthIndicator:** Available disk space
- **DataSourceHealthIndicator:** Database connectivity
- **RedisHealthIndicator:** Redis connection status
- **MailHealthIndicator:** Email server connectivity
- **ElasticsearchHealthIndicator:** Search service status

**Custom Health Indicators:**
Creating business-specific health checks:
- **External API dependency:** Check third-party service availability
- **Business logic validation:** Verify critical business rules
- **Resource availability:** Check file system, network resources
- **Configuration validation:** Ensure proper configuration

**Health Status Aggregation:**
- **UP:** All indicators are healthy
- **DOWN:** At least one critical indicator is unhealthy  
- **OUT_OF_SERVICE:** Service is intentionally out of service
- **UNKNOWN:** Health cannot be determined

### Metrics Endpoint

**Micrometer Integration:**
Actuator uses Micrometer jako metrics facade, similar to SLF4J dla logging:
- **Vendor-neutral:** Works z multiple monitoring systems
- **Dimensional metrics:** Support dla tags/labels
- **Timer support:** Latency i throughput measurements
- **Memory-efficient:** Optimized dla high-cardinality metrics

**JVM Metrics:**
Automatic collection of JVM performance data:
- **Memory utilization:** Heap, non-heap, garbage collection
- **Thread information:** Active threads, deadlock detection
- **Class loading:** Loaded classes, unloaded classes
- **CPU utilization:** System i process CPU usage

**Application Metrics:**
- **HTTP request metrics:** Request count, duration, error rates
- **Database metrics:** Connection pool status, query performance
- **Cache metrics:** Hit ratio, eviction rates
- **Custom business metrics:** Order processing rates, user activities

### Info Endpoint

**Application Metadata:**
- **Build information:** Version, build time, Git commit
- **Environment details:** Java version, operating system
- **Configuration properties:** Selected application properties
- **Custom information:** Business-specific metadata

**Dynamic Information:**
- **Runtime calculations:** Current statistics, computed values
- **Environment-specific data:** Database version, external service info
- **Feature flags:** Current feature toggle states

### Beans Endpoint

**Dependency Injection Insights:**
Complete view of Spring Application Context:
- **Bean definitions:** All registered beans
- **Dependencies:** Bean dependency graph
- **Scopes:** Singleton, prototype, request, session
- **Aliases:** Alternative names dla beans

**Troubleshooting Benefits:**
- **Missing beans:** Why expected bean wasn't created
- **Circular dependencies:** Dependency cycles detection
- **Configuration conflicts:** Multiple beans of same type
- **Conditional configuration:** Why certain configs didn't activate

### Environment Endpoint

**Configuration Sources:**
Hierarchical view of all configuration sources:
- **Command line arguments** (highest priority)
- **JNDI attributes**
- **Java system properties** 
- **OS environment variables**
- **Profile-specific configuration files**
- **Default properties** (lowest priority)

**Property Resolution:**
- **Active profiles:** Which profiles are currently active
- **Property sources:** Where each property is defined
- **Property values:** Actual values (sensitive data masked)
- **Property origin:** File i line number gdzie property is defined

## 📈 Advanced Monitoring

### Custom Metrics

**Business Metrics:**
Creating metrics that reflect business value:
- **Revenue metrics:** Sales per hour, average order value
- **User engagement:** Active users, session duration
- **Performance metrics:** Page load times, API response times
- **Error metrics:** Business process failures, validation errors

**Metric Types Deep Dive:**

**Counter:**
Monotonically increasing values:
- **Use cases:** Request counts, error counts, processed items
- **Operations:** increment(), increment(amount)
- **Best practices:** Never decrement, reset only on application restart

**Gauge:**
Point-in-time values that can go up i down:
- **Use cases:** Current memory usage, active connections, queue size
- **Operations:** set(value), increment(), decrement()
- **Implementation:** Often backed by method calls lub callback functions

**Timer:**
Measures duration i frequency:
- **Use cases:** Request processing time, method execution time
- **Metrics generated:** Count, total time, max time, percentiles
- **Best practices:** Use try-with-resources lub @Timed annotation

**Distribution Summary:**
Measures distribution of values:
- **Use cases:** Request payload sizes, response sizes
- **Metrics generated:** Count, total amount, max, percentiles
- **Configuration:** Percentiles, SLA boundaries

### Prometheus Integration

**Prometheus Metrics Format:**
- **Text-based format:** Human-readable metrics exposition
- **Time series data:** Metrics with timestamps i labels
- **Pull model:** Prometheus scrapes metrics from endpoints
- **Service discovery:** Automatic target discovery

**Metric Labels:**
Dimensional data dla better analysis:
- **Instance labels:** Server, datacenter, environment
- **Business labels:** Customer segment, product category
- **Technical labels:** HTTP method, status code, exception type

**PromQL Queries:**
- **Rate calculations:** rate(http_requests_total[5m])
- **Aggregations:** sum by(instance)(memory_usage)
- **Percentiles:** histogram_quantile(0.95, request_duration)
- **Alerting rules:** Conditions dla triggering alerts

### Grafana Dashboard Integration

**Dashboard Design Principles:**
- **Golden Signals:** Latency, traffic, errors, saturation
- **Hierarchical layout:** High-level overview → detailed views
- **Time ranges:** Multiple time windows dla trend analysis
- **Alerting integration:** Visual indicators dla alert status

**Common Dashboard Patterns:**
- **RED method:** Rate, Errors, Duration
- **USE method:** Utilization, Saturation, Errors
- **Four Golden Signals:** Google SRE methodology
- **Business KPIs:** Revenue, conversion rates, user satisfaction

## 🚨 Alerting i Incident Response

### Alert Design

**Alert Fatigue Prevention:**
- **Meaningful alerts:** Every alert should be actionable
- **Severity levels:** Critical, warning, informational
- **Escalation policies:** Who gets notified when
- **Suppression rules:** Avoid duplicate lub redundant alerts

**Service Level Objectives (SLOs):**
- **Error budget:** Acceptable failure rate over time period
- **Burn rate:** How fast error budget is consumed
- **Multi-window alerting:** Different thresholds dla different time windows

### Health Check Strategies

**Liveness vs Readiness:**
- **Liveness probe:** Is application running?
- **Readiness probe:** Is application ready to serve traffic?
- **Startup probe:** Has application finished starting up?

**Kubernetes Integration:**
- **Pod lifecycle management:** Automated restart na liveness failure
- **Service mesh integration:** Istio health checking
- **Rolling updates:** Readiness-based traffic shifting

### Graceful Shutdown

**Shutdown Hooks:**
- **Cleanup resources:** Close database connections, file handles
- **Complete in-flight requests:** Graceful request completion
- **Signal external systems:** Notify load balancers, service discovery
- **Timeout handling:** Force shutdown if graceful shutdown takes too long

## 🔒 Security Considerations

### Endpoint Security

**Sensitive Information Exposure:**
- **Configuration masking:** Hide passwords, API keys
- **Access control:** Role-based access to different endpoints
- **Network security:** Limit endpoint access to internal networks
- **Audit logging:** Log access to sensitive endpoints

**Authentication Integration:**
- **Spring Security:** Integrate z existing security configuration
- **Basic authentication:** Simple username/password protection
- **Token-based:** JWT lub OAuth2 token validation
- **mTLS:** Certificate-based authentication

### Production Hardening

**Endpoint Exposure Control:**
- **Whitelist approach:** Enable only necessary endpoints
- **Path customization:** Change default paths dla security through obscurity
- **CORS configuration:** Cross-origin resource sharing policies
- **Rate limiting:** Prevent abuse of monitoring endpoints

**Network Segregation:**
- **Management network:** Separate network dla monitoring traffic
- **Firewall rules:** Restrict access to monitoring ports
- **VPN access:** Require VPN dla external monitoring access

## 📊 Performance Monitoring

### JVM Performance

**Garbage Collection Monitoring:**
- **GC algorithms:** G1GC, Parallel GC, ZGC performance characteristics
- **Memory pools:** Eden, survivor spaces, old generation utilization
- **GC events:** Frequency, duration, impact na application
- **Memory leaks:** Growing old generation, decreasing available memory

**Thread Analysis:**
- **Thread states:** Running, waiting, blocked thread counts
- **Thread pools:** Active threads, queue sizes, rejected tasks
- **Deadlock detection:** Automatic deadlock identification
- **CPU utilization:** Thread-level CPU consumption

### Database Performance

**Connection Pool Monitoring:**
- **Active connections:** Currently in use connections
- **Pool size:** Total available connections
- **Wait time:** Time spent waiting dla available connection
- **Connection leaks:** Connections not properly returned to pool

**Query Performance:**
- **Slow query detection:** Queries exceeding thresholds
- **Query frequency:** Most executed queries
- **Transaction metrics:** Transaction duration, rollback rates
- **Lock contention:** Database lock wait times

---

## 💼 Enterprise Monitoring Strategies

### Multi-Environment Monitoring

**Environment-Specific Configurations:**
- **Development:** Verbose logging, all endpoints enabled
- **Staging:** Production-like monitoring, realistic load testing
- **Production:** Security-hardened, critical metrics only

**Centralized Monitoring:**
- **Log aggregation:** ELK stack (Elasticsearch, Logstash, Kibana)
- **Metrics aggregation:** Prometheus + Grafana
- **Distributed tracing:** Jaeger lub Zipkin
- **Incident management:** PagerDuty, OpsGenie integration

### Compliance i Audit

**Regulatory Requirements:**
- **Data retention:** How long to keep monitoring data
- **Access controls:** Who can access monitoring information
- **Audit trails:** Changes to monitoring configuration
- **Data privacy:** Sensitive information w logs i metrics

**Change Management:**
- **Monitoring as code:** Version-controlled monitoring configuration
- **Deployment tracking:** Correlation between deployments i metrics
- **Rollback procedures:** Monitoring-driven rollback decisions

---

## 🔗 Powiązane Tematy

- [[Spring Boot Performance]] - optymalizacja wydajności based na metrics
- [[Spring Boot Microservices]] - monitoring distributed systems
- [[Spring Security - Podstawy Bezpieczeństwa]] - securing actuator endpoints
- [[Spring Boot Testing - Kompletny Przewodnik]] - testing monitoring features
- [[Spring Boot Docker & Deployment]] - monitoring w containerized environments

---

*Czas nauki: ~35 minut*  
*Poziom: Średniozaawansowany*  
*Wymagana wiedza: Spring Boot basics, basic understanding of monitoring concepts*