package ma.simo.mss.controller;
import ma.simo.mss.dto.UserInfoResponse;
import ma.simo.mss.util.JwtUtils;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/auth")
public class UserController {
        @GetMapping("/me")
        public ResponseEntity<UserInfoResponse> me(Authentication authentication) {
            UserInfoResponse res = new UserInfoResponse(
                    JwtUtils.getUsername(authentication),
                    JwtUtils.getRoles(authentication)
            );
            return ResponseEntity.ok(res);
        }
    }


