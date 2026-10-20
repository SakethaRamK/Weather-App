from pathlib import Path
from PySide6.QtWidgets import QApplication,QWidget,QLabel,QVBoxLayout,QHBoxLayout,QLineEdit,QPushButton,QSizePolicy,QGraphicsOpacityEffect
from PySide6.QtCore import Qt,QPropertyAnimation,QEasingCurve
from PySide6.QtGui import QFont, QPixmap
import weather_app
url = weather_app.url
IMAGE_DIR = Path(__file__).resolve().parent / "images"
class WeatherBackground(QWidget):
    def __init__(self):
        super().__init__()
        self.weather_condition = "clear"
        self.image_paths = {
            "clear": IMAGE_DIR / "background_weather.png",
            "rain": IMAGE_DIR / "background_weather_rainy.png",
            "snow": IMAGE_DIR / "background_weather_snowy.png",
            "storm": IMAGE_DIR / "background_weather_stormy.png",
            "cloudy": IMAGE_DIR / "background_weather_cloudy.png",
            "fog": IMAGE_DIR / "background_weather_fog.png",
        }
        self.image = QPixmap()
        self.next_image = QPixmap()
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.image_label.setGeometry(self.rect())
        self.next_image_label = QLabel(self)
        self.next_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.next_image_label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.next_image_label.setGeometry(self.rect())
        self.next_image_label.hide()
        self.opacity_effect = QGraphicsOpacityEffect(self.next_image_label)
        self.opacity_effect.setOpacity(0.0)
        self.next_image_label.setGraphicsEffect(self.opacity_effect)
        self.animation = QPropertyAnimation(self.opacity_effect,b"opacity",self)
        self.animation.setDuration(800)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.finished.connect(self.finish_transition)
        self.set_condition("clear", animate=False)
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_background()
    def showEvent(self, event):
        super().showEvent(event)
        self.image_label.lower()
        if self.next_image_label.isVisible():
            self.next_image_label.raise_()
    def scale_image(self, pixmap, label):
        if pixmap.isNull():
            return
        scaled_image = pixmap.scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatioByExpanding,Qt.TransformationMode.SmoothTransformation)
        label.setPixmap(scaled_image)
        label.resize(scaled_image.size())
        x = (self.width() - scaled_image.width()) // 2
        y = (self.height() - scaled_image.height()) // 2
        label.move(x, y)
    def update_background(self):
        if not self.image.isNull():
            self.scale_image(self.image, self.image_label)
        if not self.next_image.isNull():
            self.scale_image(self.next_image,self.next_image_label)
    def finish_transition(self):
        self.animation.stop()
        self.image = self.next_image
        self.next_image = QPixmap()
        self.image_label.setGraphicsEffect(None)
        self.scale_image(self.image, self.image_label)
        self.next_image_label.hide()
        self.opacity_effect.setOpacity(0.0)
        self.image_label.lower()
        self.next_image_label.raise_()
        self.next_image_label.setGraphicsEffect(self.opacity_effect)
    def set_condition(self, condition, animate=True):
        condition = condition.lower()
        if "rain" in condition:
            key = "rain"
        elif "snow" in condition:
            key = "snow"
        elif "storm" in condition:
            key = "storm"
        elif "cloudy" in condition:
            key = "cloudy"
        elif "fog" in condition:
            key = "fog"
        else:
            key = "clear"
        image_path = self.image_paths[key]
        new_image = QPixmap(str(image_path))
        if new_image.isNull():
            print(f"Could not load image: {image_path}")
            return
        if (not self.image.isNull() and new_image.cacheKey() == self.image.cacheKey()):
            self.weather_condition = condition
            return
        self.weather_condition = condition
        if self.image.isNull() or not animate:
            self.animation.stop()
            self.next_image_label.hide()
            self.image = new_image
            self.next_image = QPixmap()
            self.image_label.setPixmap(self.image)
            self.update_background()
            self.image_label.lower()
            return
        if self.animation.state() == QPropertyAnimation.State.Running:
            self.animation.stop()
            if self.opacity_effect.opacity() >= 0.5:
                self.image = self.next_image
            self.next_image_label.hide()
            self.opacity_effect.setOpacity(0.0)
            self.image_label.setPixmap(self.image)
            self.update_background()
        self.next_image = new_image
        self.scale_image(self.next_image,self.next_image_label)
        self.opacity_effect.setOpacity(0.0)
        self.next_image_label.show()
        self.next_image_label.raise_()
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

def click():
    name = line.text().strip()
    if not name:
        check.setText("Status: Enter a city name.")
        return
    button.setEnabled(False)
    check.setText("Status: Fetching weather...")
    app.processEvents()
    try:
        params = {"name": name}
        coordinates = weather_app.get_coordinates(url, params)
        if coordinates is None:
            check.setText("Status: City not found or lookup failed.")
            return
        latitude, longitude = coordinates
        data = weather_app.get_data(latitude,longitude,name)
        if not data[0]:
            check.setText(f"Status: {data[1]}")
            return
        weather, time_data = data[1]
        check.setText(f"Status: Weather in {name}")
        temp.setText(f"Temperature: {weather['temperature']}{weather['temperature_units']}")
        humid.setText(f"Humidity: {weather['humidity']}{weather['humidity_units']}")
        speed.setText(f"Wind Speed: {weather['wind']}{weather['wind_units']}")
        condition.setText(f"Condition: {weather['condition']}")
        window.set_condition(weather["condition"])
        if time_data < 60:
            update.setText(f"Updated: {int(time_data)} seconds ago")
        else:
            update.setText(f"Updated: {int(time_data // 60)} minutes ago")
    finally:
        button.setEnabled(True)
app = QApplication([])
window = WeatherBackground()
window.setWindowTitle("Weather App")
window.resize(500, 400)
title = QLabel("Weather App")
check = QLabel("Status: Enter a city to begin.")
temp = QLabel("Temperature: --")
humid = QLabel("Humidity: --")
speed = QLabel("Wind Speed: --")
update = QLabel("Updated: --")
condition = QLabel("Condition: --")
line = QLineEdit()
line.setPlaceholderText("Enter the city name")
line.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Preferred,)
line.setStyleSheet("""
    QLineEdit {
        background-color: rgba(255, 255, 255, 190);
        color: #172033;
        border: 1px solid rgba(255, 255, 255, 210);
        border-radius: 10px;
        padding: 12px 18px;
        selection-background-color: #8BA7C5;
    }
    QLineEdit:focus {
        background-color: rgba(255, 255, 255, 225);
        border: 1px solid rgba(255, 255, 255, 255);
    }
""")
button = QPushButton("Search")
button.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Preferred,)
button.setStyleSheet("""
    QPushButton {
        background-color: rgba(255, 255, 255, 185);
        color: #26364A;
        border: 1px solid rgba(255, 255, 255, 210);
        border-radius: 10px;
        padding: 12px 18px;
        font-weight: bold;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 235);
        border: 1px solid white;
    }
    QPushButton:pressed {
        background-color: rgba(215, 225, 238, 230);
    }
    QPushButton:disabled {
        color: #777777;
    }
""")
button.clicked.connect(click)
line.returnPressed.connect(click)
posv = QVBoxLayout()
posh = QHBoxLayout()
subweather = QVBoxLayout()
title_font = QFont("Times New Roman", 20)
title_font.setWeight(QFont.Weight.Bold)
text_font = QFont("Times New Roman", 15)
text_font.setItalic(True)
title.setFont(title_font)
title.setStyleSheet("""
    QLabel {
        background-color: rgba(255, 255, 255, 145);
        color: #172033;
        border: 1px solid rgba(255, 255, 255, 190);
        border-radius: 14px;
        padding: 8px 22px;
    }
""")
for label in (check, temp, humid, speed, update, condition):
    label.setFont(text_font)
    label.setMargin(2)
    label.setStyleSheet("""
        QLabel {
            background-color: rgba(255, 255, 255, 125);
            color: #172033;
            border: 1px solid rgba(255, 255, 255, 165);
            border-radius: 10px;
            padding: 7px 12px;
        }
    """)
posh.addWidget(line, 4)
posh.addWidget(button, 1)
posv.addWidget(title,alignment=Qt.AlignmentFlag.AlignCenter,)
posv.addLayout(posh)
posv.addWidget(check)
subweather.setSpacing(10)
subweather.addWidget(condition)
subweather.addWidget(temp)
subweather.addWidget(humid)
subweather.addWidget(speed)
subweather.addWidget(update)
posv.addLayout(subweather)
posv.addStretch()
posv.setContentsMargins(15, 15, 15, 15)
posv.setSpacing(12)
window.setLayout(posv)
for widget in (title,check,temp,humid,speed,update,condition,line,button,):
    widget.raise_()
window.show()
app.exec()
