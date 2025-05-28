package com.uploader.uploader.config;

import org.springframework.amqp.core.*;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;


@Configuration
public class SenderConfig {
    @Value("${queue.name}")
    private String message;

    @Value("${rmq.exchange.name}")
    private String exchange;

    @Value("${rmq.routing.key}")
    private String routingKey;

    @Bean
    public Queue queue() {
        return new Queue(message, true);
    }

    @Bean
    DirectExchange exchange() {
        return new DirectExchange(exchange);
    }

    @Bean
    Binding binding(Queue queue, DirectExchange exchange) {
        return BindingBuilder.bind(queue).to(exchange).with(routingKey);
    }


}
