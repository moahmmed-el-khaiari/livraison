package ma.simo.order_service.Client;

import ma.simo.order_service.Dto.external.ShipmentCreateDto;
import ma.simo.order_service.Dto.external.ShipmentResponseDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(name = "shipment-service")
public interface ShipmentClient {
    @PostMapping("/shipments")
    ShipmentResponseDto createShipment(@RequestBody ShipmentCreateDto request);
}
