package com.example.demo.service;

import com.example.demo.entity.ChatHistory;
import com.example.demo.repository.ChatHistroyRepository;
import com.example.demo.repository.ChatbotRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

@Service
public class UserTriggeredService {
    @Autowired
    private ChatHistroyRepository chatHistroyRepository;

    private Timer timer;
    private final int DELAY_MILLISECONDS = 30000; // 3-초 동안 추가 호출이 없으면 실행

    public UserTriggeredService() {
        this.timer = new Timer();
    }

    public void userTriggeredMethod() {
        // 이전에 실행되던 타이머를 취소하고 새 타이머를 시작
        System.out.println("유저가 호출을 시작.");
        if (timer != null) {
            timer.cancel();
        }

        timer = new Timer();

        // 일정 시간이 지나면 실행할 작업
        timer.schedule(new TimerTask() {
            @Override
            public void run() {
                performDebouncedTask();
            }
        }, DELAY_MILLISECONDS);
    }

    private void performDebouncedTask() {
        System.out.println("유저가 호출을 중지한 시간이 지남.");
            List<ChatHistory> chatHistories=chatHistroyRepository.findByStatus(Boolean.TRUE);
        for (ChatHistory chatHistory : chatHistories) {
            chatHistory.setStatus(Boolean.FALSE);
        }
    }

}
