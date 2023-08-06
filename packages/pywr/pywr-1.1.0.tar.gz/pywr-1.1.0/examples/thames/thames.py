""" Example Pywr model using a simple reservoir system.



"""
from pywr.model import Model
from pywr.recorders import TablesRecorder
import numpy as np
from matplotlib import pyplot as plt
import click
import time


@click.group()
def cli():
    pass


@cli.command()
def run():

    # Run the model
    model = Model.load('thames.json')

    # Add a storage recorder
    TablesRecorder(model, 'thames_output.h5')

    # Run the model
    stats = model.run()
    print(stats)
    stats_df = stats.to_dataframe()
    print(stats_df)

    keys_to_plot = (
        'time_taken_before',
        'solver_stats.bounds_update_nonstorage',
        'solver_stats.bounds_update_storage',
        'solver_stats.objective_update',
        'solver_stats.lp_solve',
        'solver_stats.result_update',
        'time_taken_after',
    )

    keys_to_tabulate = (
        'timesteps',
        'time_taken',
        'solver',
        'num_scenarios',
        'speed',
        'solver_name'
        'solver_stats.total',
        'solver_stats.number_of_rows',
        'solver_stats.number_of_cols',
        'solver_stats.number_of_nonzero',
        'solver_stats.number_of_routes',
        'solver_stats.number_of_nodes',
    )

    values = []
    labels = []
    explode = []
    solver_sub_total = 0.0
    for k in keys_to_plot:
        v = stats_df.loc[k][0]
        values.append(v)
        label = k.split('.', 1)[-1].replace('_', ' ').capitalize()
        explode.append(0.0)
        if k.startswith('solver_stats'):
            labels.append('Solver - {}'.format(label))
            solver_sub_total += v
        else:

            labels.append(label)

    values.append(stats_df.loc['solver_stats.total'][0] - solver_sub_total)
    labels.append('Solver - Other')
    explode.append(0.0)

    values.append(stats_df.loc['time_taken'][0] - sum(values))
    values = np.array(values) / sum(values)
    labels.append('Other')
    explode.append(0.0)

    fig, (ax1, ax2) = plt.subplots(figsize=(12, 4), ncols=2, sharey='row',
                                   gridspec_kw={'width_ratios': [2, 1]})

    print(values, labels)
    ax1.pie(values, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    cell_text = []
    for index, value in stats_df.iterrows():
        if index not in keys_to_tabulate:
            continue
        v = value[0]
        if isinstance(v, (float, np.float64, np.float32)):
            v = f'{v:.2f}'

        cell_text.append([index, v])

    tbl = ax2.table(cellText=cell_text, colLabels=['Statistic', 'Value'], loc='center')
    tbl.scale(1.5, 1.5)  # may help
    tbl.set_fontsize(14)
    ax2.axis('off')

    fig.savefig('run_statistics_w_tables.png', dpi=300)
    fig.savefig('run_statistics_w_tables.eps')

    plt.show()


@cli.command()
@click.option('--ext', default='png')
@click.option('--show/--no-show', default=False)
def figures(ext, show):

    for name, df in TablesRecorder.generate_dataframes('thames_output.h5'):
        df.columns = ['Very low', 'Low', 'Central', 'High', 'Very high']

        fig, (ax1, ax2) = plt.subplots(figsize=(12, 4), ncols=2, sharey='row',
                                       gridspec_kw={'width_ratios': [3, 1]})
        df['2100':'2125'].plot(ax=ax1)
        df.quantile(np.linspace(0, 1)).plot(ax=ax2)

        if name.startswith('reservoir'):
            ax1.set_ylabel('Volume [$Mm^3$]')
        else:
            ax1.set_ylabel('Flow [$Mm^3/day$]')

        for ax in (ax1, ax2):
            ax.set_title(name)
            ax.grid(True)
        plt.tight_layout()

        if ext is not None:
            fig.savefig(f'{name}.{ext}', dpi=300)

    if show:
        plt.show()


if __name__ == '__main__':
    cli()
