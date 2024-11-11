package com.example.demo.entity;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDateTime;
import java.util.List;

@Entity
@NoArgsConstructor
@Getter
@Setter
@Table(name="users")
public class Users {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long userId;
    private String name;
    private LocalDateTime localDateTime;
    @OneToMany(mappedBy = "user")
    private List<ChatBot> chatBot;
    @OneToMany(mappedBy = "user")
    private List<Messages> messages;
    @OneToMany(mappedBy = "user")
    private List<ChatHistory> chatBotRepositories;

}
