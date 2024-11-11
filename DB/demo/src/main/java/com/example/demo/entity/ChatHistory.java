package com.example.demo.entity;

import jakarta.annotation.Nullable;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class ChatHistory {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long chatHistoryId;
    private String userMessage;
    private String aiResponse;
    private String aiEmotion;
    private Boolean status;
    @ManyToOne
    @JoinColumn(name="user_id")
    private Users user;
}
