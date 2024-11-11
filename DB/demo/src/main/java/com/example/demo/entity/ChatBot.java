package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Entity
@Getter
@Setter
@NoArgsConstructor
public class ChatBot {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long chatBotID;
    private String chatBotName;
    private String conversationPattern;//프롬프트에 전달되는 내용으로 chatbot의 대화 패턴을 담고 있다.
    private String conversationPoint;//프롬프트에 전달되는 내용으로 chatbot의 대화 시점을 담고 있다.
    private Boolean status;

    @ManyToOne()
    @JoinColumn(name ="user_id")
    private Users user;


}
