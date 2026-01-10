package ma.simo.order_service.Client;

import ma.simo.order_service.Dto.external.TrackingEventCreateDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
@FeignClient(name = "tracking-service")
public interface TrackingClient {
    @PostMapping("/tracking/events")
    void addEvent(@RequestBody TrackingEventCreateDto request);
}
