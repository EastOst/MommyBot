import React, { useState } from 'react';

function ChatBot() {
    const [userInput, setUserInput] = useState('');
    const [messages, setMessages] = useState([]);

    const handleSendMessage = async () => {
        // 사용자 메시지를 상태에 추가
        const newUserMessage = { text: userInput, sender: 'user' };
        setMessages((prevMessages) => [...prevMessages, newUserMessage]);

        try {
            const response = await fetch('http://localhost:8080/rasp/init', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: userInput }),
                mode: 'cors',  // CORS 모드 설정
            });

            if (!response.ok) {
                throw new Error('서버 응답 실패');
            }

            const data = await response.json();
            // 봇의 응답 메시지를 상태에 추가
            setMessages((prevMessages) => [
                ...prevMessages,
                { text: data.aiResponse, sender: 'assistant' },
            ]);
        } catch (error) {
            console.error('에러 발생:', error);
            setMessages((prevMessages) => [
                ...prevMessages,
                { text: '서버와 연결할 수 없습니다. 다시 시도해 주세요.', sender: 'assistant' },
            ]);
        } finally {
            // 사용자 입력 필드를 초기화
            setUserInput('');
        }
    };

    return (
        <div style={{ margin: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h1>마미봇 로봇 테스트</h1>
            <div style={{ border: '1px solid #aaa', padding: '10px', height: '300px', overflowY: 'scroll', marginBottom: '20px' }}>
                {messages.map((message, index) => (
                    <div key={index} style={{ margin: '10px 0', color: message.sender === 'user' ? 'gray' : 'black' }}>
                        {message.sender === 'user' ? `사용자: ${message.text}` : `로봇: ${message.text}`}
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="메시지를 입력하세요..."
                style={{ width: '80%', marginRight: '10px' }} // 입력창 스타일
            />
            <button onClick={handleSendMessage}>전송</button>
        </div>
    );
}

export default ChatBot;
