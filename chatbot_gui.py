import sys, time, requests, json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QLabel, QComboBox, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QIcon


API_URL = "http://127.0.0.1:1234/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}


class APICaller(QThread):
    update_thought = pyqtSignal(str)
    finished = pyqtSignal(str, str)

    def __init__(self, messages, model):
        super().__init__()
        self.messages = messages
        self.model = model
        self._stop = False

    def run(self):
        start_time = time.time()
        for i in range(5):
            if self._stop:
                return
            thought = f"🤖 Thinking... ({i+1}/5) [{time.time() - start_time:.2f}s]"
            self.update_thought.emit(thought)
            time.sleep(0.4)

        try:
            payload = {
                "model": self.model,
                "messages": self.messages,
                "stream": False
            }
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            data = response.json()

            full_content = data["choices"][0]["message"]["content"].strip()
            lines = full_content.strip().split("\n")
            reasoning = "\n".join(lines[:-1]).strip()
            final_output = lines[-1].strip() if lines else full_content

            self.finished.emit(reasoning, final_output)

        except Exception as e:
            self.finished.emit("", f"⚠️ Error: {str(e)}")

    def stop(self):
        self._stop = True


class ChatBubble(QWidget):
    def __init__(self, text, is_user=False):
        super().__init__()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)

        label = QLabel(text)
        label.setWordWrap(True)
        label.setFont(QFont("Segoe UI", 10))
        label.setStyleSheet(
            f"""
            background-color: {'#0078d7' if is_user else '#2c2c2c'};
            color: white;
            padding: 10px;
            border-radius: 12px;
            max-width: 400px;
            """
        )

        if is_user:
            layout.addStretch()
            layout.addWidget(label)
        else:
            layout.addWidget(label)
            layout.addStretch()

        self.setLayout(layout)
        self.setStyleSheet("background-color: transparent;")


class DeepSeekChat(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DeepSeek Chat – PyQt5")
        self.setFixedSize(600, 720)
        self.setStyleSheet("background-color: #121212; color: white;")

        self.models = ["deepseek-chat", "deepseek-coder"]
        self.selected_model = self.models[0]
        self.messages = [
            {"role": "assistant", "content": "Hello! I'm AI Assistant running locally. How can I help you today?"}
        ]

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QHBoxLayout()
        title = QLabel("🤖 DeepSeek Chat")
        title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        subtitle = QLabel("Reasoning before replying")
        subtitle.setStyleSheet("color: #aaaaaa; font-size: 10pt")

        header_info = QVBoxLayout()
        header_info.addWidget(title)
        header_info.addWidget(subtitle)

        self.model_selector = QComboBox()
        self.model_selector.addItems(self.models)
        self.model_selector.currentTextChanged.connect(self.change_model)
        self.model_selector.setStyleSheet("background-color: #2c2c2c; color: white; padding: 6px;")

        header.addLayout(header_info)
        header.addStretch()
        header.addWidget(self.model_selector)

        layout.addLayout(header)

        # Chat area
        self.chat_list = QListWidget()
        self.chat_list.setStyleSheet("background-color: transparent; border: none;")
        layout.addWidget(self.chat_list)

        self.add_bot_message(self.messages[0]["content"])

        # Thought / Typing Indicator
        self.typing_label = QLabel("")
        self.typing_label.setAlignment(Qt.AlignCenter)
        self.typing_label.setStyleSheet("color: #888; font-style: italic;")
        layout.addWidget(self.typing_label)

        # Input area
        input_layout = QHBoxLayout()
        self.input_box = QTextEdit()
        self.input_box.setFixedHeight(60)
        self.input_box.setStyleSheet("background-color: #1e1e1e; border-radius: 8px; padding: 10px; color: white;")
        input_layout.addWidget(self.input_box)

        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("background-color: #00e6cb; padding: 10px; border-radius: 8px;")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)

        layout.addLayout(input_layout)

    def change_model(self, model):
        self.selected_model = model

    def send_message(self):
        user_input = self.input_box.toPlainText().strip()
        if not user_input:
            return

        self.input_box.clear()
        self.add_user_message(user_input)
        self.messages.append({"role": "user", "content": user_input})

        self.typing_label.setText("🧠 Thinking...")

        self.thread = APICaller(self.messages, self.selected_model)
        self.thread.update_thought.connect(self.typing_label.setText)
        self.thread.finished.connect(self.show_response)
        self.thread.start()

    def show_response(self, thoughts, final):
        self.typing_label.clear()
        if thoughts:
            self.add_bot_message(f"🧠 Thoughts:\n{thoughts}")
        self.add_bot_message(final)
        self.messages.append({"role": "assistant", "content": f"{thoughts}\n{final}"})

    def add_user_message(self, text):
        item = QListWidgetItem()
        bubble = ChatBubble(text, is_user=True)
        item.setSizeHint(bubble.sizeHint())
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, bubble)
        self.chat_list.scrollToBottom()

    def add_bot_message(self, text):
        item = QListWidgetItem()
        bubble = ChatBubble(text, is_user=False)
        item.setSizeHint(bubble.sizeHint())
        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, bubble)
        self.chat_list.scrollToBottom()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DeepSeekChat()
    window.show()
    sys.exit(app.exec_())
