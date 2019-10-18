#include "QProgressIndicator.h"

#include <QPainter>
#include <QtWidgets/QStyle>
#include <QtWidgets/QApplication>
#include <QDebug>
#include <QStyleFactory>
#include <QtWidgets/QProxyStyle>
#include <QStyleOptionToolButton>
#include <QFormLayout>
#include <QDialogButtonBox>
#include <algorithm>

QProgressIndicator::QProgressIndicator(QWidget* parent, int size, int interval)
        : QWidget(parent),
        m_angle(0),
        m_timerId(-1),
        m_delay(interval),
        m_displaySize(size, size),
        m_dark(Qt::black),
        m_light(Qt::white)
{
    setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
    setFocusPolicy(Qt::NoFocus);
	m_dark = this->palette().color(QPalette::WindowText);
	m_light = this->palette().color(QPalette::Window);
}

bool QProgressIndicator::isAnimated () const
{
    return (m_timerId != -1);
}

void QProgressIndicator::setDisplaySize(QSize size)
{
	setSizeHint(size);
}
void QProgressIndicator::setSizeHint(int size)
{
	setSizeHint(QSize(size, size));
}
void QProgressIndicator::setSizeHint(QSize size)
{
    m_displaySize = size;
    update();
}




void QProgressIndicator::startAnimation()
{
    m_angle = 0;

    if (m_timerId == -1)
        m_timerId = startTimer(m_delay);
}
void QProgressIndicator::start() { startAnimation(); }

void QProgressIndicator::stopAnimation()
{
    if (m_timerId != -1)
        killTimer(m_timerId);

    m_timerId = -1;

    update();
}
void QProgressIndicator::stop() { stopAnimation(); }

void QProgressIndicator::setAnimationDelay(int delay)
{
    if (m_timerId != -1)
        killTimer(m_timerId);

    m_delay = delay;

    if (m_timerId != -1)
        m_timerId = startTimer(m_delay);
}

void QProgressIndicator::set_colors(const QColor & dark, const QColor & light)
{
    m_dark = dark; m_light = light;

    update();
}

QSize QProgressIndicator::sizeHint() const
{
    return m_displaySize;
}

int QProgressIndicator::heightForWidth(int w) const
{
    return w;
}

void QProgressIndicator::timerEvent(QTimerEvent * /*event*/)
{
    m_angle = (m_angle-2)%360;

    update();
}

void QProgressIndicator::paintEvent(QPaintEvent * /*event*/)
{
	QPainter painter(this);
	draw_snake_spinner(painter, this->rect(), m_angle, m_light, m_dark);
}

static inline QByteArray detectDesktopEnvironment()
{
    const QByteArray xdgCurrentDesktop = qgetenv("XDG_CURRENT_DESKTOP");
    if (!xdgCurrentDesktop.isEmpty())
        // See http://standards.freedesktop.org/menu-spec/latest/apb.html
        return xdgCurrentDesktop.toUpper();

    // Classic fallbacks
    if (!qEnvironmentVariableIsEmpty("KDE_FULL_SESSION"))
        return QByteArrayLiteral("KDE");
    if (!qEnvironmentVariableIsEmpty("GNOME_DESKTOP_SESSION_ID"))
        return QByteArrayLiteral("GNOME");

    // Fallback to checking $DESKTOP_SESSION (unreliable)
    const QByteArray desktopSession = qgetenv("DESKTOP_SESSION");
    if (desktopSession == "gnome")
        return QByteArrayLiteral("GNOME");
    if (desktopSession == "xfce")
        return QByteArrayLiteral("XFCE");

    return QByteArrayLiteral("UNKNOWN");
}

class CalibreStyle: public QProxyStyle {
    private:
        QHash<int, QString> icon_map;
        QByteArray desktop_environment;
        QDialogButtonBox::ButtonLayout button_layout;

    public:
        CalibreStyle(QStyle *base, QHash<int, QString> icmap) : QProxyStyle(base), icon_map(icmap) {
            setObjectName(QString("calibre"));
            desktop_environment = detectDesktopEnvironment();
            button_layout = static_cast<QDialogButtonBox::ButtonLayout>(QProxyStyle::styleHint(SH_DialogButtonLayout));
            if (QLatin1String("GNOME") == desktop_environment || QLatin1String("MATE") == desktop_environment || QLatin1String("UNITY") == desktop_environment || QLatin1String("CINNAMON") == desktop_environment || QLatin1String("X-CINNAMON") == desktop_environment)
                button_layout = QDialogButtonBox::GnomeLayout;
        }

        int styleHint(StyleHint hint, const QStyleOption *option = 0,
                   const QWidget *widget = 0, QStyleHintReturn *returnData = 0) const {
            switch (hint) {
                case SH_DialogButtonBox_ButtonsHaveIcons:
                    return 1;  // We want icons on dialog button box buttons
                case SH_DialogButtonLayout:
                    // Use platform specific button orders always
#ifdef Q_OS_WIN32
                    return QDialogButtonBox::WinLayout;
#elif defined(Q_OS_MAC)
                    return QDialogButtonBox::MacLayout;
#endif
                    return button_layout;
                case SH_FormLayoutFieldGrowthPolicy:
                    return QFormLayout::FieldsStayAtSizeHint;  // Do not have fields expand to fill all available space in QFormLayout
                default:
                    break;
            }
            return QProxyStyle::styleHint(hint, option, widget, returnData);
        }

        QIcon standardIcon(StandardPixmap standardIcon, const QStyleOption * option = 0, const QWidget * widget = 0) const {
            if (icon_map.contains(standardIcon)) return QIcon(icon_map.value(standardIcon));
            return QProxyStyle::standardIcon(standardIcon, option, widget);
        }

        int pixelMetric(PixelMetric metric, const QStyleOption * option = 0, const QWidget * widget = 0) const {
            switch (metric) {
                case PM_TabBarTabVSpace:
                    return 8;  // Make tab bars a little narrower, the value for the Fusion style is 12
                default:
                    break;
            }
            return QProxyStyle::pixelMetric(metric, option, widget);
        }

        void drawComplexControl(ComplexControl control, const QStyleOptionComplex * option, QPainter * painter, const QWidget * widget = 0) const {
            const QStyleOptionToolButton *toolbutton = NULL;
            switch (control) {
                case CC_ToolButton:
                    // We do not want an arrow if the toolbutton has an instant popup
                    toolbutton = qstyleoption_cast<const QStyleOptionToolButton *>(option);
                    if (toolbutton && (toolbutton->features & QStyleOptionToolButton::HasMenu) && !(toolbutton->features & QStyleOptionToolButton::PopupDelay)) {
                        QStyleOptionToolButton opt = QStyleOptionToolButton(*toolbutton);
                        opt.features = toolbutton->features & ~QStyleOptionToolButton::HasMenu;
                        return QProxyStyle::drawComplexControl(control, &opt, painter, widget);
                    }
                    break;
                default:
                    break;
            }
            return QProxyStyle::drawComplexControl(control, option, painter, widget);
        }

        void drawPrimitive(PrimitiveElement element, const QStyleOption * option, QPainter * painter, const QWidget * widget = 0) const {
            const QStyleOptionViewItem *vopt = NULL;
            switch (element) {
                case PE_PanelItemViewItem:
                    // Highlight the current, selected item with a different background in an item view if the highlight current item property is set
                    if (option->state & QStyle::State_HasFocus && (vopt = qstyleoption_cast<const QStyleOptionViewItem *>(option)) && widget && widget->property("highlight_current_item").toBool()) {
                        QColor color = vopt->palette.color(QPalette::Normal, QPalette::Highlight);
                        QStyleOptionViewItem opt = QStyleOptionViewItem(*vopt);
                        if (color.lightness() > 128)
                            color = color.darker(widget->property("highlight_current_item").toInt());
                        else
                            color = color.lighter(125);
                        opt.palette.setColor(QPalette::Highlight, color);
                        return QProxyStyle::drawPrimitive(element, &opt, painter, widget);
                    }
                    break;
                default:
                    break;
            }
            return QProxyStyle::drawPrimitive(element, option, painter, widget);
        }
};

int load_style(QHash<int,QString> icon_map) {
    QStyle *base_style = QStyleFactory::create(QString("Fusion"));
    QApplication::setStyle(new CalibreStyle(base_style, icon_map));
    return 0;
}

class NoActivateStyle: public QProxyStyle {
 	public:
        int styleHint(StyleHint hint, const QStyleOption *option = 0, const QWidget *widget = 0, QStyleHintReturn *returnData = 0) const {
            if (hint == QStyle::SH_ItemView_ActivateItemOnSingleClick) return 0;
            return QProxyStyle::styleHint(hint, option, widget, returnData);
        }
};

void set_no_activate_on_click(QWidget *widget) {
    widget->setStyle(new NoActivateStyle);
}

class TouchMenuStyle: public QProxyStyle {
    private:
        int extra_margin;

    public:
        TouchMenuStyle(int margin) : extra_margin(margin) {}
        QSize sizeFromContents ( ContentsType type, const QStyleOption * option, const QSize & contentsSize, const QWidget * widget = 0 ) const {
            QSize ans = QProxyStyle::sizeFromContents(type, option, contentsSize, widget);
            if (type == QStyle::CT_MenuItem) {
                ans.setHeight(ans.height() + extra_margin);  // Make the menu items more easily touchable
            }
            return ans;
        }
};

void set_touch_menu_style(QWidget *widget, int margin) {
    widget->setStyle(new TouchMenuStyle(margin));
}

void draw_snake_spinner(QPainter &painter, QRect rect, int angle, const QColor & light, const QColor & dark) {
	painter.save();
    painter.setRenderHint(QPainter::Antialiasing);
    if (rect.width() > rect.height()) {
        int delta = (rect.width() - rect.height()) / 2;
        rect = rect.adjusted(delta, 0, -delta, 0);
	} else if (rect.height() > rect.width()) {
        int delta = (rect.height() - rect.width()) / 2;
        rect = rect.adjusted(0, delta, 0, -delta);
	}
    int disc_width = std::max(3, std::min(rect.width() / 10, 8));
    QRect drawing_rect(rect.x() + disc_width, rect.y() + disc_width, rect.width() - 2 * disc_width, rect.height() - 2 *disc_width);
    int gap = 60;  // degrees
    QConicalGradient gradient(drawing_rect.center(), angle - gap / 2);
    gradient.setColorAt((360 - gap/2)/360.0, light);
    gradient.setColorAt(0, dark);

    QPen pen(QBrush(gradient), disc_width);
    pen.setCapStyle(Qt::RoundCap);
    painter.setPen(pen);
    painter.drawArc(drawing_rect, angle * 16, (360 - gap) * 16);
	painter.restore();
}
