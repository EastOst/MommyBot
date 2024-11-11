package com.example.demo.repository;

import com.example.demo.entity.ChatBot;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChatbotRepository extends JpaRepository<ChatBot,Long> {
    ChatBot findByStatus(Boolean status);
}
