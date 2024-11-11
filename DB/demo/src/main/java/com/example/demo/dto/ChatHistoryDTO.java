package com.example.demo.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class ChatHistoryDTO {
    private String userMessage;
    private String aiResponse;
    private String Emotion;
    private Long userId;  // 외래 키를 위한 사용자 ID
}

