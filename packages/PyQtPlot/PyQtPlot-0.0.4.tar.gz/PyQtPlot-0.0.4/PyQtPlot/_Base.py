from collections import defaultdict
from math import cos, sin, ceil, sqrt, floor
from operator import xor
from typing import Dict, Callable, List, Tuple

from PyQt5.QtCore import QRect, Qt, QPoint, QPointF, QRectF, QSizeF, QSize
from PyQt5.QtGui import QPainter, QColor, QFontMetrics, QPainterPath, QFont, QPaintEvent, QBrush, QMouseEvent, QPen, \
    QPolygon, QPolygonF
from PyQt5.QtWidgets import QWidget


class _TooltipPreparedData:
    def __init__(self, rect, x, y, name, color):
        self.rect: QRect = rect
        self.x: int = x
        self.y: int = y
        self.name: str = name
        self.color: QColor = color


class _PlotsDict(dict):
    def __init__(self, parent, **kwargs):
        super().__init__(**kwargs)
        self.parent: _AbstractGraphicView = parent

    def ticks(self, orientation):
        return range(ceil(self.max(orientation)) + 1)

    def max(self, orientation):
        def y():
            return max([i.max_y() for i in self.values()])

        def x():
            return max([i.max_x() for i in self.values()])

        if self.parent.grid.style() == Grid.FREE:
            if orientation == _Axis.VERTICAL:
                return y()

            if orientation == _Axis.HORIZONTAL:
                return x()
        if self.parent.grid.style() == Grid.EQUAL:
            return max(y(), x())


class _AbstractGraph:
    default_brush = QBrush(QColor(255, 128, 0))
    default_pen = QPen(QColor(0, 0, 0))

    _size: float = None

    def __init__(self, data, name: str, parent: '_AbstractGraphicView', color: QColor = None):
        self.data = data
        self.parent: _AbstractGraphicView = parent
        self.name = name

        if color:
            self._color = color
            self.default_brush = QBrush(color)
            self.default_pen = QPen(color)

        self.brush = None

        self.rectangles: List[_TooltipPreparedData] = []

    def paint_event(self, painter: QPainter, echo=None):
        self.before_paint()
        new_echo = self.paint(painter, echo)
        self.after_paint()
        return new_echo

    def paint(self, painter: QPainter, echo=None) -> Dict:
        raise NotImplementedError()

    def before_paint(self):
        self.rectangles = []

    def after_paint(self):
        pass

    def color(self) -> QColor:
        return self._color

    def get_brush(self) -> QBrush:
        if self.brush is None:
            return self.default_brush
        return self.brush

    def pen(self) -> QPen:
        return self.default_pen

    def check_mouse(self, x: int, y: int, figure: QRect):
        self.rectangles.append(_TooltipPreparedData(figure, x, y, self.name, self._color))

    def mouse_move(self, pos: QPoint, out: List[Tuple[QPoint, int, int, str, QColor]]):
        for data in self.rectangles:
            if isinstance(data.rect, (QRect, QRectF)):
                if data.rect.contains(pos):
                    out.append((pos, data.x, data.y, data.name, data.color))
            elif isinstance(data.rect, (QPolygon, QPolygonF)):
                if data.rect.containsPoint(pos, Qt.WindingFill):
                    out.append((pos, data.x, data.y, data.name, data.color))

    def size(self):
        if self._size is not None:
            return self._size
        return self.parent.plot_size()

    def max_y(self):
        return max([i for i in self.data.values()])

    def max_x(self):
        return max([i for i in self.data.keys()])


class _Line(_AbstractGraph):
    _area_width = 20

    def paint(self, painter: QPainter, echo=None):
        painter.setPen(self.pen())
        previous_x, previous_y = None, None
        start = QPoint(self.parent.margin_left(), self.parent.height() - self.parent.margin_top())
        x_interval = self.parent.horizontal_ax.tick_interval()
        y_interval = self.parent.vertical_ax.tick_interval()
        for x, y in self.data.items():
            if previous_x is not None:
                a = start + QPoint(previous_x * x_interval, -previous_y * y_interval)
                b = start + QPoint(x * x_interval, -y * y_interval)
                painter.drawLine(a, b)
                length = sqrt(pow(a.x() - b.x(), 2) + pow(a.y() - b.y(), 2))
                c = self._area_width / length
                c_x = c * (b.x() - a.x())
                c_y = c * (b.y() - a.y())

                bounds = [QPointF(a.x() + c_x, a.y() - c_y),
                          QPointF(b.x() + c_x, b.y() - c_y),
                          QPointF(b.x() - c_x, b.y() + c_y),
                          QPointF(a.x() - c_x, a.y() + c_y)]

                polygon = QPolygonF(bounds)

                self.rectangles.append(
                    _TooltipPreparedData(
                        polygon,
                        x,
                        y,
                        self.name,
                        self.color()
                    )
                )

            previous_x, previous_y = x, y

    def mouse_move(self, pos: QPoint, out: List[Tuple[QPoint, int, int, str, QColor]]):
        for data in self.rectangles:
            if isinstance(data.rect, (QRect, QRectF)):
                if data.rect.contains(pos):
                    out.append((pos, data.x, data.y, data.name, data.color))
                    return
            elif isinstance(data.rect, (QPolygon, QPolygonF)):
                if data.rect.containsPoint(pos, Qt.WindingFill):
                    out.append((pos, data.x, data.y, data.name, data.color))
                    return


class _Scatter(_AbstractGraph):
    default_brush = QBrush(QColor(255, 128, 0))

    def paint(self, painter: QPainter, echo=None):
        size = self.size()
        painter.setBrush(self.get_brush())
        start = QPoint(self.parent.margin_left(), self.parent.height() - self.parent.margin_top())
        for x, y in self.data.items():
            rect = QRect(
                start + QPoint(
                    x * self.parent.horizontal_ax.tick_interval() - size / 2,
                    -y * self.parent.vertical_ax.tick_interval() - size / 2
                ),
                QSize(size, size)
            )
            painter.drawEllipse(
                rect
            )

            self.check_mouse(x, y, rect)

    def __init__(self, data, name, parent, color: QColor = None):
        if isinstance(data, list):
            data = {i: value for i, value in enumerate(data)}
        super().__init__(data, name, parent, color)


class _Bar(_AbstractGraph):
    def __init__(self, data: Dict[int, int], name: str, parent, color: QColor = None, stacked=False):
        super().__init__(data, name, parent, color)

        self.stacked = stacked
        self._width = 0.75
        self._nested_width = 0
        self._offset = 0

    def paint(self, painter, echo=None):
        margin_left = self.parent.margin_left()

        for bar, h in self.data.items():
            x_pos = margin_left + self.parent.horizontal_ax.ticks().index(bar) \
                    * self.parent.horizontal_ax.tick_interval()

            height = int(h * self.parent.vertical_ax.tick_interval())
            width = self.parent.horizontal_ax.tick_interval() * self.width()

            if self.stacked:
                y_offset = echo[bar]
                echo[bar] += height
            else:
                y_offset = 0

            rect = QRect(
                x_pos + (1 - self.real_width() + self.offset() * 2) * self.parent.horizontal_ax.tick_interval() / 2,
                int(self.parent.horizontal_ax.y_pos() - y_offset),
                width,
                -height)
            self.check_mouse(bar, h, rect)
            painter.fillRect(
                rect,
                self.color()
            )

        return echo

    def set_width(self, val):
        self._width = val

    def width(self):
        if self._nested_width == 0:
            return self._width
        else:
            return self._nested_width

    def set_color(self, val):
        self._color = val

    def set_offset(self, val):
        self._offset = val

    def offset(self):
        return self._offset

    def set_nested_width(self, val):
        self._nested_width = val

    def real_width(self):
        return self._width


class _Axis:
    orientation: int
    VERTICAL = 0
    HORIZONTAL = 1

    _min_tick_interval = 30
    _tick_skip = [1, 2, 5, 10, 25, 100, 1000]
    _real_ticks: List[int] = None

    def __init__(self, parent, **kwargs):
        self.width = parent.width
        self.height = parent.height
        self.parent: _AbstractGraphicView = parent

        self._ticks = None
        self._tick_count = None
        self._tick_width = 6
        self._tick_interval = None
        self._ticks_margin = 0
        self._tick_rotation = 0
        self._y_pos = None
        self._size = None
        self._unit = ""

    def _paint_label(self, painter: QPainter):
        raise NotImplementedError()

    def paint(self, painter):
        raise NotImplementedError()

    def set_ticks(self, val):
        self._ticks = val

    def ticks(self):
        if self._ticks is not None:
            return self._ticks

        return self.parent.plots.ticks(self.orientation)

    def real_ticks(self):
        return self._real_ticks

    def _set_tick_interval(self, val):
        self._tick_interval = val

    def tick_interval(self):
        return self._tick_interval

    def set_tick_margin(self, val):
        self._ticks_margin = val

    def tick_margin(self):
        return self._ticks_margin

    def y_pos(self):
        return self._y_pos

    def _set_y_pos(self, val):
        self._y_pos = val

    def _set_size(self, val):
        self._size = val

    def size(self):
        return self._size

    def _set_tick_count(self, val):
        self._tick_count = val

    def tick_count(self):
        return self._tick_count

    def tick_rotation(self):
        return self._tick_rotation

    def set_tick_rotation(self, val):
        self._tick_rotation = val

    def tick_width(self):
        return self._tick_width

    def set_label(self, text: str):
        self._unit = text

    def label(self) -> str:
        return self._unit


class _HorizontalAxis(_Axis):
    orientation = _Axis.HORIZONTAL

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self._offset = 0

    def paint(self, painter):
        self._real_ticks = []

        width = self.width()
        height = self.height()
        margin_right = self.parent.margin_right()
        margin_bottom = self.parent.margin_bottom()
        margin_left = self.parent.margin_left()

        self._set_tick_count(len(self.ticks()))
        self._set_size(width - margin_left - margin_right)
        self._set_tick_interval(self.size() / self.tick_count())
        self._set_y_pos(height - margin_bottom)

        tick_interval = self.tick_interval()
        skip = 0
        while self._tick_skip[skip] * tick_interval < self._min_tick_interval:
            skip += 1

        y_pos = self.y_pos()
        tick_width = self.tick_width()

        for i in range(self.tick_count()):
            if skip != 0 and i % self._tick_skip[skip] != 0:
                continue
            x_pos = margin_left + (i + self.offset()) * tick_interval
            self._real_ticks.append(x_pos)
            painter.drawLine(x_pos, y_pos - tick_width / 2, x_pos, y_pos + tick_width / 2)

            if self.tick_rotation() != 0:
                painter.translate(x_pos, y_pos + tick_width / 2 + 4)
                painter.rotate(-self.tick_rotation())
                painter.translate(-x_pos, -(y_pos + tick_width / 2 + 4))
                painter.drawText(
                    QRect(
                        x_pos - tick_interval / 2 + self.tick_margin() * cos(self.tick_rotation()) - 20,
                        y_pos + (tick_width / 2 + 4) * cos(self.tick_rotation()) - self.tick_margin() * sin(
                            self.tick_rotation()),
                        50,
                        30),
                    xor(Qt.AlignHCenter, Qt.AlignVCenter),
                    str(self.ticks()[i])
                )
                painter.resetTransform()
            else:
                painter.drawText(
                    QRect(
                        x_pos - self.tick_interval() / 2,
                        y_pos + tick_width / 2 + 4 + self.tick_margin(),
                        40,
                        20),
                    Qt.AlignHCenter,
                    str(self.ticks()[i])
                )

        self._paint_label(painter)

    def _paint_label(self, painter: QPainter):
        if self.label() != "":
            painter.drawText(
                QRect(
                    self.width() - self.parent.margin_left() - self.parent.margin_right(),
                    self.y_pos(),
                    200,
                    50,
                ),
                xor(Qt.AlignRight, Qt.AlignTop),
                self.label()
            )

    def offset(self):
        return self._offset

    def set_offset(self, val):
        self._offset = val


class _VerticalAxis(_Axis):
    orientation = _Axis.VERTICAL

    def __init__(self, parent: '_AbstractGraphicView', **kwargs):
        super().__init__(parent, **kwargs)

    def paint(self, painter):
        self._real_ticks = []

        width = self.width()
        height = self.height()
        top, right = self.parent.margin_top(), self.parent.margin_right()
        bottom, left = self.parent.margin_bottom(), self.parent.margin_left()

        painter.drawLine(left, top, left, height - bottom)
        painter.drawLine(left, height - bottom, width - right, height - bottom)

        ticks = self.ticks()

        self._set_tick_count(ticks[-1] - ticks[0] + 1)
        self._set_size(height - bottom - bottom)
        self._set_tick_interval(self.size() / self.tick_count())

        tick_interval = self.tick_interval()
        skip = 0
        while self._tick_skip[skip] * tick_interval < self._min_tick_interval:
            skip += 1

        for i in range(self.tick_count()):
            if skip != 0 and i % self._tick_skip[skip] != 0:
                continue
            if i in ticks:
                y_pos = (height - bottom) - i * tick_interval
                self._real_ticks.append(y_pos)
                painter.drawLine(left - self.tick_width() / 2, y_pos, left + self.tick_width() / 2, y_pos)

                painter.drawText(
                    QRect(0, y_pos - 10, left - self.tick_width() / 2 - 4, 20),
                    xor(Qt.AlignVCenter, Qt.AlignRight),
                    str(i))

        self._paint_label(painter)

    def _paint_label(self, painter: QPainter) -> None:
        if self.label() != "":
            painter.drawText(
                QRect(
                    0,
                    0,
                    self.parent.margin_right(),
                    self.parent.margin_top()
                ),
                xor(Qt.AlignBottom, Qt.AlignRight),
                self.label()
            )


class Margin:
    ABSOLUTE = 0
    RELATIVE = 1

    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3

    def __init__(self, value, mode=RELATIVE):
        self.value = value
        self.mode = mode

    def get(self, size):
        if self.mode == Margin.ABSOLUTE:
            return self.value
        if self.mode == Margin.RELATIVE:
            return size * self.value


class Grid:
    _default_color: QColor = QColor(80, 80, 80, 80)
    _color: QColor = None

    EQUAL = 1
    FREE = 0
    _style: int = FREE

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self._color = kwargs.get('grid_color', None)

        self._show_vertical = kwargs.get('grid_vertical', False)
        self._show_horizontal = kwargs.get('grid_horizontal', False)

    def paint(self, painter):
        painter.setPen(QPen(self.color()))
        if self.horizontal():
            x_start = self.parent.margin_left()
            x_end = self.parent.width() - self.parent.margin_right()
            for y_pos in self.parent.vertical_ax.real_ticks():
                painter.drawLine(QPoint(x_start, y_pos), QPoint(x_end, y_pos))

        if self.vertical():
            y_start = self.parent.margin_top()
            y_end = self.parent.height() - self.parent.margin_bottom()
            for x_pos in self.parent.horizontal_ax.real_ticks():
                painter.drawLine(x_pos, y_start, x_pos, y_end)

    def horizontal(self):
        return self._show_horizontal

    def show_horizontal(self, val: bool):
        self._show_horizontal = val

    def vertical(self):
        return self._show_vertical

    def show_vertical(self, val: bool):
        self._show_vertical = val

    def color(self):
        if self._color is not None:
            return self._color
        return self._default_color

    def set_color(self, color: QColor):
        self._color = color

    def style(self):
        return self._style

    def set_style(self, val):
        self._style = val


class _AbstractGraphicView(QWidget):
    plot_type = _AbstractGraph

    _default_colors = [QColor(255, 128, 0), QColor(0, 0, 255), QColor(255, 0, 0), QColor(0, 255, 0)]
    _default_tooltip_brush = QBrush(QColor(255, 255, 255, 80))

    _default_plot_size: int

    def __init__(self, flags=None, *args, **kwargs):
        super().__init__(flags, *args)

        if kwargs.get('data', False):
            if kwargs.get('name', False):
                self.add_plot(kwargs.get('data'), kwargs.get('name'))

        self.margins = [Margin(0.1), Margin(0.1), Margin(0.1), Margin(0.1)]

        self.setMouseTracking(True)
        self._mouse_pos = QPoint(0, 0)

        self.tooltips = []
        self._tooltip_func: Callable[[str, int, str], str] = lambda text, bar, plot_name: None
        self._tooltip_count = 0
        self._tooltip_horizontal_offset = 10

        self.horizontal_ax = _HorizontalAxis(self, **kwargs)
        self.vertical_ax = _VerticalAxis(self, **kwargs)
        self.grid = Grid(self, **kwargs)

        self.plots: _PlotsDict[str, _AbstractGraph] = _PlotsDict(self)

        self.color = QColor(255, 128, 0)
        self.bg_color = QColor(255, 255, 255)

        self.item_color = QColor(255, 128, 0)

        self.item_width = 0.75

        self.font = QFont()
        self.font.setPixelSize(20)

        self.legend_font = QFont()
        self.legend_font.setPixelSize(14)

    def _define_color(self, color):
        if color is not None:
            return color
        else:
            return self._default_colors[len(self.plots.items()) % len(self._default_colors)]

    # %update data
    def update_data(self, data, name):
        self.plots[name] = _Bar(data, name, self, self.plots[name].color())

        self.repaint()

    # %mouse event

    def mouse_pos(self):
        return self._mouse_pos

    def mouseMoveEvent(self, event: QMouseEvent):
        pos = QPoint(int(event.localPos().x()), int(event.localPos().y()))
        for plot in self.plots.values():
            plot.mouse_move(pos, self.tooltips)

        current = len(self.tooltips)
        if current > 0 or current != self._tooltip_count or (self._tooltip_count > 0 and current == 0):
            self._tooltip_count = len(self.tooltips)
            self.repaint()

    # %paint

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter()
        painter.begin(self)

        painter.setFont(self.font)

        self._paint_background(painter)

        self.vertical_ax.paint(painter)
        self.horizontal_ax.paint(painter)
        self.grid.paint(painter)

        plot_echo = defaultdict(int)
        for plot in self.plots.values():
            plot_echo = plot.paint_event(painter, plot_echo)

        vertical_offset = 0
        while len(self.tooltips):
            vertical_offset += self._paint_tooltip(painter, *self.tooltips.pop(), vertical_offset)

        self._show_legend(painter)

        painter.end()

    def _paint_background(self, painter):
        width = self.width()
        height = self.height()

        painter.fillRect(0, 0, width, height, self.bg_color)

    # %tooltip

    def set_tooltip_func(self, func: Callable[[str, int, str], str]):
        self._tooltip_func = func

    def _show_tooltip(self, rect, text, bar, plot_name):
        self.tooltips.append((rect, text, bar, plot_name))

    def _show_legend(self, painter: QPainter):
        fm = QFontMetrics(self.legend_font)
        width = fm.width(max(self.plots.keys(), key=lambda x: len(x))) + fm.height()
        height = fm.height() * len(self.plots)

        body_rect = QRectF(
            QPointF(self.width() - 4 - width-10, 4),
            QSizeF(
                width + 10,
                height + 10
            )
        )

        path = QPainterPath()
        path.addRoundedRect(body_rect, 10., 10.)

        painter.fillPath(path, QColor(0, 0, 0, 40))
        painter.drawPath(path)

        row = 0
        for name, plot in self.plots.items():
            row += 1
            painter.fillRect(
                body_rect.x() + 2,
                body_rect.y() + 4 + (row - 1) * fm.height(),
                fm.height() - 1,
                fm.height() - 1,
                plot.color()
            )
            painter.setBrush(QColor(255, 255, 255))
            painter.setFont(self.legend_font)
            painter.drawText(
                QRect(
                    body_rect.x() + 4 + fm.height(),
                    body_rect.y() + 2 + (row - 1) * fm.height(),
                    width - 8 - 2,
                    fm.height()
                ),
                xor(Qt.AlignVCenter, Qt.AlignLeft),
                name
            )

    def _paint_tooltip(self, painter: QPainter, point: QPoint, y: int, x: int, plot_name: str,
                       color: QColor, vertical_offset: int) -> int:
        painter.setPen(QPen(QColor(40, 40, 40)))
        res = self._tooltip_func(y, x, plot_name)
        painter.setBrush(self._default_tooltip_brush)
        point = QPoint(point.x() + self._tooltip_horizontal_offset, point.y() + vertical_offset)
        color = QColor(
            min(color.red() * 1.4, 255),
            min(color.green() * 1.4, 255),
            min(color.blue() * 1.4, 255),
            200)

        if res is not None:
            lines: List = res.split('\n')
            lengths = [len(l) for l in lines]

            fm = QFontMetrics(self.font)
            width = fm.width(lines[lengths.index(max(lengths))])
            height = fm.height() * len(lines)

            path = QPainterPath()
            path.addRoundedRect(
                QRectF(
                    QPointF(point.x() - 5, point.y() - 5),
                    QSizeF(
                        width + 10,
                        height + 10
                    )
                ), 10., 10.)

            painter.fillPath(
                path,
                color)
            painter.drawPath(path)

            painter.drawText(
                QRect(
                    point,
                    QSize(
                        width,
                        height
                    )
                ),
                xor(Qt.AlignLeft, Qt.AlignTop),
                res)

            return height + 11
        return 0

    # %plot

    def add_plot(self, data, name, color=None) -> str:
        self.plots[name] = self.plot_type(data, name, self, color=self._define_color(color))
        return name

    def plot_size(self):
        return self._default_plot_size

    # %margin

    def set_margin(self, *args):
        if len(args) == 1:
            m = Margin(args[0])
            self.margins = [m for _ in range(4)]

        elif len(args) == 2:
            lef_right = Margin(args[0])
            top_bottom = Margin(args[1])
            self.margins = [top_bottom, lef_right, top_bottom, lef_right]

        elif len(args) == 3:
            self.margins = [Margin(args[0]), Margin(args[1]), Margin(args[2]), Margin(args[1])]

        elif len(args) == 4:
            self.margins = [Margin(i) for i in args]

        else:
            raise ValueError('args length is bigger than 4')

    def margin_left(self):
        return self.margins[Margin.LEFT].get(self.width())

    def margin_right(self):
        return self.margins[Margin.RIGHT].get(self.width())

    def margin_top(self):
        return self.margins[Margin.TOP].get(self.height())

    def margin_bottom(self):
        return self.margins[Margin.BOTTOM].get(self.height())
