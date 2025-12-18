package ma.simo.mss.security;
import org.springframework.core.convert.converter.Converter;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.jwt.Jwt;

import java.util.*;
import java.util.stream.Collectors;
public class JwtAuthConverter implements Converter<Jwt, Collection<GrantedAuthority>>  {

    /**
     * Keycloak met souvent les rôles dans:
     * - realm_access.roles : ["ADMIN","CLIENT",...]
     *
     * Ce converter transforme ça en:
     * - ROLE_ADMIN, ROLE_CLIENT, ...
     */


        @Override
        public Collection<GrantedAuthority> convert(Jwt jwt) {

            // 1) Récupérer realm_access.roles
            Map<String, Object> realmAccess = jwt.getClaim("realm_access");
            if (realmAccess == null) return List.of();

            Object rolesObj = realmAccess.get("roles");
            if (!(rolesObj instanceof Collection<?> roles)) return List.of();

            // 2) Transformer en ROLE_*
            return roles.stream()
                    .filter(Objects::nonNull)
                    .map(Object::toString)
                    .map(String::trim)
                    .filter(r -> !r.isEmpty())
                    .map(r -> r.startsWith("ROLE_") ? r : "ROLE_" + r)
                    .map(SimpleGrantedAuthority::new)
                    .collect(Collectors.toSet());
        }
    }


