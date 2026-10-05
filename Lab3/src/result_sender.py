from abc import ABC, abstractmethod


class ResultSender(ABC):

    @abstractmethod
    def send(self, message):
        """Отправляет строку с результатом сторонней системе."""


class EmailResultSender(ResultSender):

    def send(self, message):
        print(f"[Имитация email-сервера] Отправлено сообщение: {message}")
        return True

