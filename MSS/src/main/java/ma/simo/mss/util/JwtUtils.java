package ma.simo.mss.util;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;

import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
public final class JwtUtils {
        private JwtUtils() {}

        /**
         * Username depuis JWT Keycloak :
         * - preferred_username (souvent présent)
         * - sinon subject
         */
        public static String getUsername(Authentication auth) {
            Jwt jwt = getJwt(auth);
            if (jwt == null) return null;

            String preferred = jwt.getClaimAsString("preferred_username");
            if (preferred != null && !preferred.isBlank()) return preferred;

            return jwt.getSubject();
        }

        /**
         * Rôles depuis Authorities Spring (ROLE_ADMIN, ROLE_CLIENT...)
         * générés par JwtAuthConverter.
         */
        public static List<String> getRoles(Authentication auth) {
            if (auth == null || auth.getAuthorities() == null) return List.of();
            return auth.getAuthorities().stream()
                    .map(GrantedAuthority::getAuthority)
                    .sorted()
                    .collect(Collectors.toList());
        }

        /**
         * (Optionnel) lire directement realm_access.roles si besoin.
         */
        public static List<String> getRealmRoles(Authentication auth) {
            Jwt jwt = getJwt(auth);
            if (jwt == null) return List.of();

            Map<String, Object> realmAccess = jwt.getClaim("realm_access");
            if (realmAccess == null) return List.of();

            Object rolesObj = realmAccess.get("roles");
            if (!(rolesObj instanceof List<?> roles)) return List.of();

            return roles.stream().map(Object::toString).collect(Collectors.toList());
        }

        private static Jwt getJwt(Authentication auth) {
            if (auth == null) return null;
            Object principal = auth.getPrincipal();
            if (principal instanceof Jwt jwt) return jwt;
            return null;
        }
    }


