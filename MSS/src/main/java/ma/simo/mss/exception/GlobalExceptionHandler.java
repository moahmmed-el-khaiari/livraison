package ma.simo.mss.exception;
import jakarta.servlet.http.HttpServletRequest;
import ma.simo.mss.dto.ErrorResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.core.AuthenticationException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import java.time.Instant;

@RestControllerAdvice
public class GlobalExceptionHandler {



        @ExceptionHandler(UnauthorizedException.class)
        public ResponseEntity<ErrorResponse> handleUnauthorized(UnauthorizedException ex, HttpServletRequest req) {
            return build(HttpStatus.UNAUTHORIZED, "UNAUTHORIZED", ex.getMessage(), req.getRequestURI());
        }

        @ExceptionHandler(AuthenticationException.class)
        public ResponseEntity<ErrorResponse> handleAuth(AuthenticationException ex, HttpServletRequest req) {
            return build(HttpStatus.UNAUTHORIZED, "UNAUTHORIZED", "Authentification requise.", req.getRequestURI());
        }

        @ExceptionHandler(AccessDeniedException.class)
        public ResponseEntity<ErrorResponse> handleDenied(AccessDeniedException ex, HttpServletRequest req) {
            return build(HttpStatus.FORBIDDEN, "FORBIDDEN", "Accès interdit (rôle insuffisant).", req.getRequestURI());
        }

        @ExceptionHandler(Exception.class)
        public ResponseEntity<ErrorResponse> handleGeneric(Exception ex, HttpServletRequest req) {
            return build(HttpStatus.INTERNAL_SERVER_ERROR, "INTERNAL_ERROR", ex.getMessage(), req.getRequestURI());
        }

        private ResponseEntity<ErrorResponse> build(HttpStatus status, String error, String message, String path) {
            ErrorResponse body = new ErrorResponse(
                    Instant.now(),
                    status.value(),
                    error,
                    message,
                    path
            );
            return ResponseEntity.status(status).body(body);
        }
    }


