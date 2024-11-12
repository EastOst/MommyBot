package com.example.demo.repository;

import com.example.demo.entity.ChatHistory;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ChatHistroyRepository extends JpaRepository<ChatHistory,Long> {
    List<ChatHistory> findByStatus(Boolean bool);
}
