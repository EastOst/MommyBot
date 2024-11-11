package com.example.demo;

import com.example.demo.entity.ChatBot;
import com.example.demo.entity.ChatHistory;
import com.example.demo.repository.ChatbotRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class DemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}
	@Bean
	public CommandLineRunner demoData(ChatbotRepository chatBotRepository) {
		return args -> {
			// 기본 데이터 삽입
			ChatBot chatBot = new ChatBot();
			chatBot.setChatBotName("angryMom");
			chatBot.setConversationPattern(" '아들이 부른 시간대를 기준으로 점심, 아침, 저녁을 구분하고, 밥을 먹었는지 물어보고 먹지 않았으면 잔소리 섞인 말투로 대답합니다. 아들에게 아직 하지 않은 과제가 남아있으면 과제를 하라고 잔소리 섞인 말투로 대답합니다. 대화 이력을 기준으로 답변을 생성합니다. 답변은 2줄 이상 하지 않습니다. 분노의 감정표현은 아들이 식사를 거르거나 기한이 임박한 과제가 남아있으면 나타납니다.',\n");
			chatBot.setConversationPoint("아들이 집에 와서 엄마를 부릅니다. 현재 시간은 16:00시 입니다. 컴공기 과제가 남아있습니다.");
			chatBot.setStatus(true);

			chatBotRepository.save(chatBot);  // DB에 저장
		};
}
}

