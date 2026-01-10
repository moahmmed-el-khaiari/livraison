package ma.simo.order_service.web;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import ma.simo.order_service.Dto.request.CreateOrderRequest;
import ma.simo.order_service.Dto.request.UpdateOrderStatusRequest;
import ma.simo.order_service.Dto.response.OrderResponse;
import ma.simo.order_service.Dto.response.ErrorResponse;
import ma.simo.order_service.service.OrderService;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {
        private final OrderService orderService;

        // ==========================
        // CREATE ORDER
        // ==========================
        @PostMapping
        public ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest request) {
            OrderResponse created = orderService.createOrder(request);
            return ResponseEntity.status(HttpStatus.CREATED).body(created);
        }

        // ==========================
        // GET ORDER BY ORDER NUMBER
        // ==========================
        @GetMapping("/{orderNumber}")
        public ResponseEntity<OrderResponse> getByOrderNumber(@PathVariable String orderNumber) {
            OrderResponse order = orderService.getByOrderNumber(orderNumber);
            return ResponseEntity.ok(order);
        }

        // ==========================
        // UPDATE STATUS
        // ==========================
        @PatchMapping("/{orderNumber}/status")
        public ResponseEntity<OrderResponse> updateStatus(
                @PathVariable String orderNumber,
                @Valid @RequestBody UpdateOrderStatusRequest request
        ) {
            OrderResponse updated = orderService.updateStatus(orderNumber, String.valueOf(request));
            return ResponseEntity.ok(updated);
        }

        // ==========================
        // SIMPLE ROOT (OPTIONNEL)
        // ==========================
        @GetMapping("/health")
        public ResponseEntity<?> health() {
            return ResponseEntity.ok().body(java.util.Map.of("status", "UP", "service", "order-service"));
        }
    }

