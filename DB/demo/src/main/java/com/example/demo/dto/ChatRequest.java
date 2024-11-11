package com.example.demo.dto;

import com.example.demo.entity.ChatBot;
import com.example.demo.entity.ChatHistory;
import com.example.demo.entity.Messages;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;
import lombok.ToString;

import java.util.List;

@NoArgsConstructor
@Setter
@ToString
@Getter
public class ChatRequest {
    private ChatBot chatBot;
    private Messages messages;
    private List<ChatHistory> chatHistoryies;
}
