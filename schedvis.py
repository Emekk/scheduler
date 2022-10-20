from typing import Sized
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe


class SchedVis:
    """A versatile class providing visualization support for schedules."""
    CMAP: mpl.colors.ListedColormap = mpl.cm.tab20

    def gantt_chart(self,
        yticklabels: Sized,
        xticklabels: Sized,
        xranges: list[list[tuple]],
        bar_height: float,
        bar_spacing: float,
        facecolors: list[list[tuple]],
        line_color: tuple,
        line_width: float,
        horizon_facecolor: tuple,
        horizon_width: float,
        bar_labels: list[list],
        bar_label_color: tuple,
        bar_label_fontsize: float | None,
        xlabel: str,
        ylabel: str,
        xtickrotation: float,
        ytickrotation: float,
        grid: bool,
        figure_size: tuple,
        font_size: float,
        xmargin: float,
        padding: float,
        bgcolor: tuple,
        show: bool,
        save_file: str,
        dpi: int,
    ) -> None:
        """Plots a gantt chart for the schedule."""
        fig, gnt = plt.subplots(figsize=figure_size)
        # set x and y limits and add margins
        gnt.set_ylim(0, len(yticklabels) * (bar_height + bar_spacing) - bar_spacing)
        gnt.set_xlim(0 - xmargin, horizon_width + xmargin)
        # set axes labels
        gnt.set_xlabel(xlabel)
        gnt.set_ylabel(ylabel)
        # set yticks
        gnt.set_yticks([i * (bar_height + bar_spacing) + bar_height / 2  for i in range(len(yticklabels))])
        gnt.set_yticklabels(yticklabels, rotation=ytickrotation, va="center", fontsize=font_size, weight="bold")
        gnt.set_xticks(range(0, int(horizon_width + 1), int(horizon_width // len(xticklabels) + 1)))
        gnt.set_xticklabels(xticklabels, rotation=xtickrotation, ha="center", fontsize=font_size, weight="bold")
        # draw bars
        for i, xrng in enumerate(xranges):
            ystart = i * (bar_height + bar_spacing)
            # draw bar representing the planning horizon
            gnt.barh(left=0, width=horizon_width, y=ystart + bar_height / 2, height=bar_height, facecolor=horizon_facecolor,
                     edgecolor=line_color, linewidth=line_width)
            # draw bars representing the tasks
            gnt.broken_barh(xranges=xrng, yrange=(ystart, bar_height), facecolor=facecolors[i], edgecolor=line_color, 
                            linewidth=line_width)
            # add bar labels
            for j, (x1, x2) in enumerate(xrng):
                # add line breaks at the positions of whitespaces
                bar_labels[i][j] = bar_labels[i][j].replace(' ', '\n')
                gnt.text(x=x1+x2/2, y=ystart+bar_height/2, s=bar_labels[i][j], horizontalalignment="center", verticalalignment="center",
                         color=bar_label_color, rotation=90, path_effects=[pe.withStroke(linewidth=line_width, foreground=line_color)], 
                         fontsize=bar_label_fontsize, multialignment="center", style="italic")
        # plot settings
        gnt.grid(grid)
        gnt.set_facecolor(bgcolor)
        fig.set_facecolor(bgcolor)
        plt.tight_layout(pad=padding)
        # show figure
        if show:
            plt.show()
        # save figure
        if save_file != "":
            fig.savefig(save_file, dpi=dpi)
