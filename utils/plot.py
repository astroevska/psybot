import io
import pandas as pd
import seaborn as sns

from datetime import date
from matplotlib import axes, figure
from matplotlib.patches import Patch
from aiogram.types import BufferedInputFile
from typing import Any, Optional, List, Set

from init.globals import globals
from constants.config import LEGEND_POSITION_Y
from constants.types import TInterpretor, TResultDF


def setPlotResultRange(
    ax: axes, color: Set[float],
    legendLabels: List[Optional[Patch]],
    label: str,
) -> List[Patch]:
    ax.text(
        0.1, 
        LEGEND_POSITION_Y, 
        globals.result, 
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

def setPlotRanges(ax: axes, ranges: List[TInterpretor]) -> axes:    
    colorCount: int = len(ranges)
    colorStep: int = 1/colorCount
    legendLabels: List[Patch] = []
    
    for r in range(len(ranges)):
        color = (colorStep*(r + 1), colorStep*(colorCount - r - 1), 0.0, 0.5)
        ax.axhspan(ranges[r][0], ranges[r][1] + 1, facecolor=color)
        
        if globals.resultIndex == r:
            legendLabels = setPlotResultRange(ax, color, legendLabels, ranges[r][2])
            continue

        legendLabels.insert(0, Patch(
            facecolor=color,
            label=ranges[r][2]
        ))

    ax.legend(handles=legendLabels, bbox_to_anchor=(1, LEGEND_POSITION_Y), loc='lower right')

    return ax

def editPlotFigure(ax: axes, **args: Any) -> figure:
    plot: figure = ax.get_figure()
    try:
        if "align" in args: plot.align = args['align']
    finally:
        return plot
    
def savePlot(plot: figure) -> BufferedInputFile:
    buf = io.BytesIO()
    plot.savefig(buf, format='png', bbox_inches="tight")
    buf.seek(0)

    return BufferedInputFile(buf.read(), filename="file.png")

def getPlot(ranges: List[TInterpretor], isStyled: bool) -> axes:
    df: TResultDF = pd.DataFrame(
        {
            "result": [globals.result],
            "date": [date.today()]
        }
    )

    ax = sns.pointplot(data = df, x = "date", y = "result", join=True)
    ax.set(ylim=(0, ranges[-1][1]), title="Динамика психологического состояния")

    if isStyled: return setPlotRanges(ax, ranges)
    return ax