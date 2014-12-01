import wpf

from System.Windows import Application, Window
from System.Windows.Markup import XamlReader
from System import Random, Math
from System.Windows import Point
from System.Windows.Controls import Canvas, UserControl
from System.Windows.Media import CompositionTarget, Brushes

def LoadXaml_str(filename):
    f = open(filename)
    try:
        element = f.read()
    finally:
        f.close()
    return element

class Snowflake(UserControl):
    def __init__(self, xaml, randomNumber):
        self.xaml = xaml
        self.randomNumber = randomNumber
        self.x = 0
        self.y = 0
        self.xSpeed = 0
        self.ySpeed = 0
        self.radius = 0
        self.scale = 0
        self.alpha = 0
        self.stageSize = Point()
        self.Content = XamlReader.Parse(xaml)
            
        # This method gets called many times a second and is responsible for moving your snowflake around
        def MoveSnowFlake(sender, e):
            self.x = self.x + self.xSpeed
            self.y = self.y + self.ySpeed
    
            Canvas.SetTop(self, self.y)
            Canvas.SetLeft(self, Canvas.GetLeft(self) + self.radius * Math.Cos(self.x))
    
            # Reset the position to go back to the top when the bottom boundary is reached
            if (Canvas.GetTop(self) > self.stageSize.Y):
                Canvas.SetTop(self, - self.ActualHeight - 10)
                self.y = Canvas.GetTop(self)

        CompositionTarget.Rendering += MoveSnowFlake # !
                     
    def SetInitialProperties(self, stageWidth, stageHeight):
        self.xSpeed = self.randomNumber.NextDouble() / 20
        self.ySpeed = .01 + self.randomNumber.NextDouble() * 2
        self.radius = self.randomNumber.NextDouble()
        self.scale = .01 + self.randomNumber.NextDouble() * 2
        self.alpha = .1 + self.randomNumber.NextDouble()
    
        # Setting initial position
        Canvas.SetLeft(self, self.randomNumber.Next(stageWidth))
        Canvas.SetTop(self, self.randomNumber.Next(stageHeight))
    
        self.stageSize = Point(stageWidth, stageHeight)
        self.y = Canvas.GetTop(self)
    
        # Setting initial size and opacity
        self.Content.Width = 5 * self.scale
        self.Content.Height = 5 * self.scale
        self.Content.Opacity = self.alpha


class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'WpfApplicationSnow.xaml')

        _snowflake = LoadXaml_str("SnowFlake.xaml")
        randomNumber = Random()
        for i in range(0, 200):
            snowflake = Snowflake(_snowflake, randomNumber)
            # 600 and 300 is the width/height of the application
            snowflake.SetInitialProperties(600, 300)
            self.LayoutRoot.Children.Add(snowflake)

if __name__ == '__main__':
    Application().Run(MyWindow())
