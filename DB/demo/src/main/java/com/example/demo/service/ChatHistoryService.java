package com.example.demo.service;

import com.example.demo.dto.ChatHistoryDTO;
import com.example.demo.dto.ChatRequest;
import com.example.demo.entity.ChatBot;
import com.example.demo.entity.ChatHistory;
import com.example.demo.entity.Messages;
import com.example.demo.entity.Users;
import com.example.demo.repository.ChatHistroyRepository;
import com.example.demo.repository.ChatbotRepository;
import com.example.demo.repository.UsersRepository;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.HttpHeaders;  // 이 임포트가 있는지 확인

import java.util.List;

@Service
@Slf4j
public class ChatHistoryService {
    @Autowired
    private UsersRepository usersRepository;
    @Autowired
    private ChatHistroyRepository chatHistroyRepository;

    @Autowired
    private ChatbotRepository chatbotRepository;
    //Message 객체를 입력받고 파이썬 플라스크와 통신후에 chatHistory를 반환
    public ChatHistoryDTO sendUserMessageToAi(Messages messages){
            System.out.println("send ai 이전 서비스계층: "+messages);
            ChatBot chatBot=chatbotRepository.findByStatus(Boolean.TRUE);//수정필요
            List<ChatHistory> chatHistories=chatHistroyRepository.findAll();//수정필요
            Messages messages1=messages;
            String url="http://localhost:5000/chat";
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            ChatRequest chatRequest=new ChatRequest();
            chatRequest.setMessages(messages1);
            chatRequest.setChatBot(chatBot);
            chatRequest.setChatHistoryies(chatHistories);
            System.out.println("====파이썬에게 보내는 데이터 형식:"+chatRequest);
        // 요청 바디 설정 (메시지를 JSON 형식으로 전달)
        // messages 객체를 JSON으로 직렬화하여 요청 본문에 담음
            HttpEntity<ChatRequest> entity = new HttpEntity<>(chatRequest, headers);

        // RestTemplate을 사용하여 POST 요청 보내기
            RestTemplate restTemplate = new RestTemplate();
            ResponseEntity<ChatHistoryDTO> response = restTemplate.exchange(url, HttpMethod.POST, entity, ChatHistoryDTO.class);
        // Emotion은 빈상태 이다.
            ChatHistoryDTO chatHistoryDTO=response.getBody();
            return response.getBody();//emotion은 빈상태로 들어온다.
    }


}
