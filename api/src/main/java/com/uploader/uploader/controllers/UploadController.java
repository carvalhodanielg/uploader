package com.uploader.uploader.controllers;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.amqp.core.Binding;
import org.springframework.amqp.core.Exchange;
import org.springframework.amqp.core.Queue;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/upload")
@RequiredArgsConstructor
public class UploadController {

    private final RabbitTemplate rabbitTemplate;
    private final ObjectMapper  objectMapper;

    private final Queue queue;
    private final Exchange exchange;

    @Value("${rmq.routing.key}")
    private String routingKey;

    @PostMapping
    public ResponseEntity<Map<String, String>> uploadFile(@RequestParam("file") MultipartFile file) throws IOException {
        String file_id = UUID.randomUUID().toString();
        Map<String, Object> message = new HashMap<>();

        message.put("file_id", file_id);
        message.put("file_name", file.getOriginalFilename());
        message.put("file_size", file.getSize());
        message.put("file_type", file.getContentType());
        message.put("data", Base64.getEncoder().encodeToString(file.getBytes()));

        rabbitTemplate.convertAndSend(this.exchange.getName(), routingKey, objectMapper.writeValueAsString(message));

        Map<String, String> response = new HashMap<>();
        response.put("file_id", file_id);
        response.put("status",  "processing");

        return ResponseEntity.ok().body(response);
    }

}
