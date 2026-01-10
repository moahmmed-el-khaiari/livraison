package ma.simo.order_service.config;

import feign.RequestInterceptor;
import feign.RequestTemplate;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.web.context.request.RequestContextHolder;
import org.springframework.web.context.request.ServletRequestAttributes;

@Configuration
public class FeignConfig {

    // Timeout Feign (en ms) – simple et fiable
    @Bean
    public feign.Request.Options feignRequestOptions() {
        return new feign.Request.Options(
                3000,  // connectTimeout
                8000   // readTimeout
        );
    }

    /**
     * Interceptor : récupère le JWT de la requête entrante
     * et le propage vers les appels Feign (shipment-service / tracking-service).
     *
     * ⚠️ Si tu n'utilises pas JWT côté services Python, tu peux supprimer ce bean.
     */
    @Bean
    public RequestInterceptor bearerTokenForwarder() {
        return new RequestInterceptor() {
            @Override
            public void apply(RequestTemplate template) {
                ServletRequestAttributes attrs =
                        (ServletRequestAttributes) RequestContextHolder.getRequestAttributes();

                if (attrs == null) return;

                HttpServletRequest request = attrs.getRequest();
                String authHeader = request.getHeader("Authorization");

                if (authHeader != null && authHeader.startsWith("Bearer ")) {
                    template.header("Authorization", authHeader);
                }
            }
        };
    }
}
