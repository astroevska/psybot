import io
import seaborn as sns
import matplotlib.dates as mdates

from matplotlib import axes, figure
from matplotlib.patches import Patch
from typing import Any, Optional, List, Set
from aiogram.types import BufferedInputFile, User

from ..db.get import getResults
from ..init.globals import globalsList
from ..utils.helpers import get2dPlotData
from ..constants.types import TInterpretor
from ..constants.config import LEGEND_POSITION_Y
from ..utils.bot.globals import getOrSetCurrentGlobal, getPreviousResult


def setPlotResponsibleAxesX(ax: axes):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=1, maxticks=6))
    ax.xaxis.set_minor_locator(mdates.AutoDateLocator())


def setPlotResultRange(
    ax: axes,
    color: Set[float],
    legendLabels: List[Optional[Patch]],
    label: str,
    result: int,
    haveResultLabel=False
) -> List[Patch]:

    if haveResultLabel:
        ax.text(
            0.1,
            LEGEND_POSITION_Y,
            result,
            fontsize=78,
            color=color,
            horizontalalignment='center',
            verticalalignment='bottom',
            transform=ax.transAxes
        )

    legendLabels.insert(0, Patch(
        facecolor=color,
        label=label,
        edgecolor=f'{"black"}'
    ))

    return legendLabels


def setPlotRanges(ax: axes, ranges: List[TInterpretor], isCurrent: bool, resultIndex: int, result: int) -> axes:
    colorCount: int = len(ranges)
    colorStep: int = 1/colorCount
    legendLabels: List[Patch] = []

    for r in range(len(ranges)):
        color = (colorStep*(r + 1), colorStep*(colorCount - r - 1), 0.0, 0.5)
        ax.axhspan(ranges[r][0], ranges[r][1] + 1, facecolor=color)

        if isCurrent and resultIndex == r:
            legendLabels = setPlotResultRange(ax, color, legendLabels, ranges[r][2], result, True)
            continue

        legendLabels.insert(0, Patch(
            facecolor=color,
            label=ranges[r][2]
        ))

    ax.legend(handles=legendLabels, bbox_to_anchor=(1, LEGEND_POSITION_Y), loc='lower right')


def editPlotFigure(ax: axes, **args: Any) -> figure:
    plot: figure = ax.get_figure()

    try:
        if "align" in args:
            plot.align = args['align']
    finally:
        return plot


def savePlot(plot: figure) -> BufferedInputFile:
    buf = io.BytesIO()
    plot.savefig(buf, format='png', bbox_inches="tight")
    buf.seek(0)
    plot.clear()

    return BufferedInputFile(buf.read(), filename="file.png")


async def getPlot(ranges: List[TInterpretor], testName: str, user: User, isCurrent: bool = True, isResponsibleX: bool = True) -> axes:
    globalsIdx = await getOrSetCurrentGlobal(user)

    if isCurrent and globalsList[globalsIdx].result == 0 and len(globalsList[globalsIdx].data) == 0:
        getPreviousResult(globalsIdx, user.id, testName)

    ax: axes = sns.pointplot(**get2dPlotData(getResults, {"telegram_id": user.id, "test_name": testName}, {
                             'x': 'date', 'y': 'result'}, isCurrent, globalsList[globalsIdx].result), join=True)
    ax.set(ylim=(0, ranges[-1][1]), title=testName)

    setPlotRanges(ax, ranges, isCurrent,
                  globalsList[globalsIdx].resultIndex, globalsList[globalsIdx].result)

    if isResponsibleX:
        setPlotResponsibleAxesX(ax)

    return ax


async def getPlotImg(user: User, isCurrent: bool):
    globalsIdx = await getOrSetCurrentGlobal(user)

    plot = await getPlot(globalsList[globalsIdx].currentTest['content']['interpretor'],
        globalsList[globalsIdx].currentTest["name"], user, isCurrent, isResponsibleX=True)

    return savePlot(editPlotFigure(plot, align="center"))
