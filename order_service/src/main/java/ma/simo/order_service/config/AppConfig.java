package ma.simo.order_service.config;

import org.springframework.context.annotation.Bean;

import java.time.Clock;

public class AppConfig {
    @Bean
    public Clock clock() {
        return Clock.systemUTC();
    }

}
