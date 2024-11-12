package com.example.demo.controller;

import com.example.demo.dto.ChatHistoryDTO;
import com.example.demo.entity.ChatHistory;
import com.example.demo.entity.Messages;
import com.example.demo.repository.ChatHistroyRepository;
import com.example.demo.repository.MessageRepository;
import com.example.demo.repository.UsersRepository;
import com.example.demo.service.ChatHistoryService;
import com.example.demo.service.UserTriggeredService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/rasp")
public class RaspberryController {
    @Autowired
    private ChatHistoryService chatHistoryService;
    @Autowired
    private ChatHistroyRepository chatHistroyRepository;

    @Autowired
    private UserTriggeredService userTriggeredService;

    @PostMapping("/init")
    @CrossOrigin(origins = "http://localhost:3000")  // React 프론트엔드가 실행되는 주소

    public ChatHistory initMessage(@RequestBody Messages message){
        //메세지 호출 완료
        System.out.println("sendAi이전"+message);
        ChatHistoryDTO chatHistoryDTO =chatHistoryService.sendUserMessageToAi(message);

        System.out.println("ai 응답처리 성공.");
        ChatHistory chatHistory=new ChatHistory();
        chatHistory.setAiResponse(chatHistoryDTO.getAiResponse());
        chatHistory.setUserMessage(chatHistoryDTO.getUserMessage());
        chatHistroyRepository.save(chatHistory);
        System.out.println("데이터 저장 성공-----응답 ");
        userTriggeredService.userTriggeredMethod();



        return chatHistory;
    }


}
