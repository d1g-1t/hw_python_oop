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

    def get_message(self) -> str:
        """Возвращает строку сообщения."""
        message = (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч. "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч. "
            f"Потрачено ккал: {self.calories:.3f}."
        )
        return str(message)


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

    def get_distance(self) -> float:
        """Получить пройденную дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        distance = self.get_distance()
        mean_speed = distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return 0  # в базовом классе не будет формулы расчета
        # соженных калорий, они будут указаны в дочерних классах

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        info_message = InfoMessage(
            self.__class__.__name__,
            self.duration,
            distance,
            mean_speed,
            calories
        )
        return info_message


class Running(Training):
    """Тип тренировки: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # Коэффициент учёта сожжёных каллорий
    # в зависимости от скорости движения
    CALORIES_MEAN_SPEED_SHIFT = 1.79     # Константа сжигаемых каллорий
    # вне зависимости от скорости движения

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        mean_speed = self.get_mean_speed()
        calories = (
            (self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
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
    # из км/ч в м/с
    CM_IN_M = 100  # константа для перевода сантиметров в метры

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height    # добавляется параметр значения роста человека
        # для учёта в формуле расчета каллорий

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при спортивной ходьбе."""
        mean_speed = self.get_mean_speed() * self.KM_PER_HOUR_TO_M_PER_SEC
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
    LEN_STEP = Training.LEN_STROKE  # константа для расчета расстояния

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

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        mean_speed = self.length_pool * self.count_pool / \
            self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при плавании."""
        mean_speed = self.get_mean_speed()
        calories = (
            (mean_speed + self.MEAN_SPEED_INCREASE)
            * self.MEAN_SPEED_MULTIPLIER * self.weight
            * self.duration
        )
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    action = data[0]
    duration = data[1]
    weight = data[2]

    if workout_type in workout_types:
        if workout_type == 'SWM':
            length_pool = data[3]
            count_pool = data[4]
            return workout_types[workout_type](action, duration, weight,
                                               length_pool, count_pool)
        elif workout_type == 'RUN':
            return workout_types[workout_type](action, duration, weight)
        elif workout_type == 'WLK':
            height = data[3]
            return workout_types[workout_type](action, duration,
                                               weight, height)
    return Training(action, duration, weight)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
