PFont minutesFont;
PFont arrivingBusTextFont;
PFont dueFont;
PFont minFont;
int windowWidth = width;
int windowHeight = height;
int minimumDimension;

int backgroundColor = #0066FF;
int minutesColor = #EEEEEE;
int secondsColor = #A1D7FF;
int textColor = #EEEEEE;

boolean debugging = false;
//visualisingBus = true;
String fontTypeface = "sans-serif";

float divider1 = windowHeight / 5;
float divider2 = windowHeight * (5.0/6.0);

// Variables for holding view strings
var minutes;
var seconds;
var arrivingBusText;
var busDestinationText;


void setup() {
  jProcessingJS(this, {
    fullscreen:true
     }
  );
  background(0, 0, 0, 0);
}

void draw() {
  if (visualisingBus && isBusDisplayed()) {
    updateWindowSize();
    updateDividerSize();

    updateArrivingBusInfo();
    updateFontsSize();

    if (minutes < 0) {
      minutes = 0;
    }

    if (seconds < 0) {
      seconds = 0;
    }

    background(0, 0, 0, 0);
    drawMinutesCounter(minutes);
    //drawDebugLines();
    drawArrivingBusText(arrivingBusText);
    drawDestinationText(busDestinationText);
    drawSecondsCounter(seconds);
  }
}

void mousePressed() {
  showMainPage();
}


void updateArrivingBusInfo() {
   if (debugging) {
      minutes = int((mouseX / float(windowWidth)) * 15);
      seconds = (mouseY / float(windowHeight)) * 60;
      arrivingBusText = "Debugging!"
      busDestinationText = "Hello";
    } else {
      seconds = window.arrivingBus.exactSecondsUntilArrival(); //secondsUntilNextBus(); //int((mouseY / float(windowHeight)) * 360);
      minutes = window.arrivingBus.minutesUntilArrival();
      arrivingBusText = "Route " + window.arrivingBus.routeNumber() + " departing " + window.busStop.address();
      busDestinationText = "Terminating at " + window.arrivingBus.destination();
    }
}

void drawMinutesCounter(int minutes) {

  int betweenDiv1Div2 = (divider2 - divider1);
  int numberY = divider1 + (betweenDiv1Div2 * 0.44);
  int dueY = divider1 + (betweenDiv1Div2 * 0.47);
  int minutesY = divider1 + (betweenDiv1Div2 * 0.7);
  fill(minutesColor);
  textAlign(CENTER, CENTER);

  if (minutes < 1) {
    textFont(dueFont);
    text("due", windowWidth / 2, dueY);

  } else {
    textFont(minutesFont);
    text(minutes, windowWidth / 2, numberY);
    textFont(minFont);
    text("minutes", windowWidth / 2, minutesY);
  }
}

void drawArrivingBusText(String arrivingBusText) {
  textFont(arrivingBusTextFont);
  textMode(SCREEN);
  smooth();
  fill(255);

  int fontWidth = windowWidth / 1.5;
  int sidePadding = int((windowWidth - fontWidth) / 2.0);
  text(arrivingBusText, sidePadding, 0, fontWidth, divider1);
}

// Make canvas not display when loading
void drawDestinationText(String busDestinationText) {
  textFont(arrivingBusTextFont);
  textMode(SCREEN);
  smooth();
  fill(255);

  int fontWidth = windowWidth / 1.5;
  int sidePadding = int((windowWidth - fontWidth) / 2.0);
  text(busDestinationText, sidePadding, windowHeight/2.5, fontWidth, windowHeight);
}

void drawDebugLines() {
  float divider1 = windowHeight / 5;
  float divider2 = windowHeight * (5.0/6.0);

  drawDividerLine(divider1);
  drawDividerLine(divider2);
}

void drawDividerLine(int y) {
  strokeWeight(minimumDimension / 150);
  stroke(230);
  line(0, y, windowWidth, y);
}

void drawSecondsCounter(int seconds) {
  stroke(secondsColor);
  strokeWeight(windowHeight / 90);
  smooth();
  strokeCap(SQUARE);
  noFill();
  int angle = (seconds / 60) * 360;
  drawArcGraphic(angle, int(minimumDimension / 1.3));
}

void updateWindowSize() {
  if (windowWidth != width || windowHeight != height) {
    windowWidth = width;
    windowHeight = height; 

    if (windowHeight < windowWidth) {
      minimumDimension = windowHeight;
    } else {
      minimumDimension = windowWidth;
    }
  }
}

void updateDividerSize() {
  divider1 = windowHeight / 5;
  divider2 = windowHeight * (5.0/6.0);
}

void drawArcGraphic(int angle, int size) {

  float fromAngle = radians(-90);
  float toAngle = radians(angle -  90);

  int middlex = int(windowWidth / 2);
  int middley = (divider1 + divider2) / 2;
  int arcSize = int((divider2 - divider1) / 1.3);

  arc( middlex, middley, arcSize,arcSize, fromAngle, toAngle);
}

void updateFontsSize() {
  minutesFont = createFont(fontTypeface, windowHeight / 3.2);
  arrivingBusTextFont = createFont(fontTypeface,windowWidth / 18);
  dueFont = createFont(fontTypeface,windowHeight / 5);
  minFont = createFont(fontTypeface,windowHeight / 22);
}