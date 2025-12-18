package ma.simo.mss.config;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.List;

@Configuration
public class AppConfig {
    /**
         * CORS global (Angular -> Spring Boot)
         * Ajuste les origins si nécessaire (prod).
         */
        @Bean
        public CorsConfigurationSource corsConfigurationSource() {
            CorsConfiguration cfg = new CorsConfiguration();

            // Front Angular (dev). Ajoute ton domaine prod ensuite.
            cfg.setAllowedOrigins(List.of(
                    "http://localhost:4200"
            ));

            // Méthodes autorisées
            cfg.setAllowedMethods(List.of(
                    HttpMethod.GET.name(),
                    HttpMethod.POST.name(),
                    HttpMethod.PUT.name(),
                    HttpMethod.PATCH.name(),
                    HttpMethod.DELETE.name(),
                    HttpMethod.OPTIONS.name()
            ));

            // Headers autorisés (JWT, content-type, etc.)
            cfg.setAllowedHeaders(List.of(
                    HttpHeaders.AUTHORIZATION,
                    HttpHeaders.CONTENT_TYPE,
                    HttpHeaders.ACCEPT,
                    "X-Requested-With"
            ));

            // Headers exposés au client (si besoin)
            cfg.setExposedHeaders(List.of(
                    HttpHeaders.AUTHORIZATION
            ));

            // Si tu utilises cookies (pas obligatoire avec Bearer JWT)
            cfg.setAllowCredentials(true);

            // Cache du preflight
            cfg.setMaxAge(3600L);

            UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
            source.registerCorsConfiguration("/**", cfg);
            return source;
        }

}
