class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def __str__(self) -> str:
        """Возвращает строку сообщения."""
        message = (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65     # длина одного шага в метрах
    LEN_STROKE = 1.38   # длина одного гребка в метрах
    M_IN_KM = 1000      # константа для перевода пройденного
    # расстояния из метров в километры
    HOURS_TO_MINUTES = 60  # программа получает время в часах
    # добавляем константу для перевода часов в минуты

    def __init__(
        self,
        action: int,      # action - количество шагов или гребков
        duration: float,  # за тренировку
        weight: float
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    @property
    def distance(self) -> float:
        """Получить пройденную дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    @property
    def mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.distance / self.duration

    @property
    def spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 0  # в базовом классе не будет формулы расчета
        # соженных калорий, формулы будут указаны в дочерних классах

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.distance,
            speed=self.mean_speed,
            calories=self.spent_calories
        )
        return info_message


class Running(Training):
    """Тип тренировки: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # коэффициент учёта сожжёных каллорий
    # в зависимости от скорости движения
    CALORIES_MEAN_SPEED_SHIFT = 1.79     # константа сжигаемых каллорий
    # вне зависимости от скорости движения

    @property
    def spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * self.mean_speed
             + self.CALORIES_MEAN_SPEED_SHIFT)
            * self.weight / self.M_IN_KM
            * (self.duration * self.HOURS_TO_MINUTES)
        )
        return calories


class SportsWalking(Training):
    """Тип тренировки: спортивная ходьба."""
    CALORIES_WEIGHT_MULPIPLIER = 0.035  # коэффициант для учета веса в процессе
    # сжигания каллорий при ходьбе
    CALORIES_HEIGHT_MULTIPLIER = 0.029  # коэффициент для учета роста в
    # процессе сжигания каллорий при ходьбе
    KM_PER_HOUR_TO_M_PER_SEC = 0.278    # константа для перевода значений
    # скорости из км/ч в м/с
    CM_IN_M = 100  # константа для перевода сантиметров в метры

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height    # добавляем параметр значения роста человека
        # для учёта в формуле расчета каллорий

    @property
    def spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        mean_speed = self.mean_speed * self.KM_PER_HOUR_TO_M_PER_SEC
        height_in_meters = self.height / self.CM_IN_M
        calories = (
            (self.CALORIES_WEIGHT_MULPIPLIER * self.weight
                + (mean_speed ** 2 / height_in_meters)
                * self.CALORIES_HEIGHT_MULTIPLIER * self.weight)
            * (self.duration * self.HOURS_TO_MINUTES)
        )
        return calories


class Swimming(Training):
    """Тип тренировки: плавание."""
    MEAN_SPEED_INCREASE = 1.1   # константа для смещения значения
    # средней скорости
    MEAN_SPEED_MULTIPLIER = 2  # константа увеличения скорости движения
    LEN_STEP = Training.LEN_STROKE  # константа для расчета дистанции

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # параметр длины бассейна в метрах
        self.count_pool = count_pool    # параметр со значением, сколько раз
        # человек переплыл бассейн за тренировку

    @property
    def mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        mean_speed = (
            self.length_pool * self.count_pool
            / self.M_IN_KM
            / self.duration
        )
        return mean_speed

    @property
    def spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        calories = (
            (self.mean_speed + self.MEAN_SPEED_INCREASE)
            * self.MEAN_SPEED_MULTIPLIER * self.weight
            * self.duration
        )
        return calories


WORKOUT_TYPES = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_class = WORKOUT_TYPES.get(workout_type, Training)
    return workout_class(*data)


def main(training: Training) -> str:
    """Главная функция."""
    info = training.show_training_info()
    print(str(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
