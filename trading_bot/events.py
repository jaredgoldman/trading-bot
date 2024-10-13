from enum import Enum, auto


class TradingEventType(Enum):
    """
    Enum class for trading events.
    """

    # Market data events
    PRICE_UPDATE = auto()
    VOLUME_UPDATE = auto()
    ORDER_BOOK_UPDATE = auto()

    # Order-related events
    ORDER_PLACED = auto()
    ORDER_FILLED = auto()
    ORDER_PARTIALLY_FILLED = auto()
    ORDER_CANCELLED = auto()

    # Account events
    BALANCE_UPDATE = auto()
    POSITION_UPDATE = auto()

    # Trading strategy events
    SIGNAL_GENERATED = auto()
    STRATEGY_START = auto()
    STRATEGY_STOP = auto()

    # System events
    CONNECTION_ESTABLISHED = auto()
    CONNECTION_LOST = auto()
    ERROR = auto()

    # Risk Management events
    RISK_CHECK_PASSED = auto()
    RISK_CHECK_FAILED = auto()
