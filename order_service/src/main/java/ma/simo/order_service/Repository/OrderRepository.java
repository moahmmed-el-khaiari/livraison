package ma.simo.order_service.Repository;

import ma.simo.order_service.entity.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {

    // 🔎 Recherche par numéro de commande
    Optional<Order> findByOrderNumber(String orderNumber);

    // 🔎 Recherche par tracking number (shipment-service)
    Optional<Order> findByTrackingNumber(String trackingNumber);

    // 🔎 Vérifier l’unicité du numéro de commande
    boolean existsByOrderNumber(String orderNumber);
}
