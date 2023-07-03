import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm


def make_boxplot(sub_df_list, title, fig):
    # Establish figure size.

    sub_df_os, sub_df_dist, sub_df_hw, sub_df_py = sub_df_list

    # We can create subplots, which allows us to have multiple subplots in the same plot.
    # plt.subplot(3, 1, 1) means we have 3 rows, 1 column, and are referencing plot 1.
    #
    ax1 = plt.subplot(2, 2, 1)
    sns.boxplot(sub_df_os['OS'], sub_df_os['Score'], ax=ax1)
    ax1.set_xlabel("Operating Systems")
    ax1.set_ylabel("Performance Score")
    # ax1.set_title(title)

    # plt.subplot(3, 1, 2) means we have 3 rows, 1 column, and are referencing plot 2.
    ax2 = plt.subplot(2, 2, 2)
    sns.boxplot(sub_df_dist['OS'], sub_df_dist['Score'], ax=ax2)
    ax2.set_xlabel("Linux Distributions")
    ax2.set_ylabel("Performance Score")
    # ax2.set_title(title)

    # plt.subplot(3, 1, 3) means we have 3 rows, 1 column, and are referencing plot 3.
    ax3 = plt.subplot(2, 2, 3)
    sns.boxplot(sub_df_hw['Hardware'], sub_df_hw['Score'], ax=ax3)
    ax3.set_xlabel("CPU Architectures")
    ax3.set_ylabel("Performance Score")
    # ax3.set_title(title)

    ax4 = plt.subplot(2, 2, 4)
    sns.boxplot(sub_df_py['Python'], sub_df_py['Score'], order=["3.6", "3.7", "3.8"], ax=ax4)
    ax4.set_xlabel("Python Versions")
    ax4.set_ylabel("Performance Score")
    # ax4.set_title(title)

    plt.suptitle(f"Project: {title}", fontsize=15)

    plt.tight_layout();  # adds more space

    # plt.savefig(f'{title}_books_read.jpg')
    return fig


def create_sub_dfs(proj_df):
    ### OS

    sub_df_os = proj_df.loc[((proj_df['OS'] == 'Linux-Xenial') &
                             (proj_df['Python'] == '3.7') &
                             (proj_df['Hardware'] == 'amd64')) |
                            (proj_df['OS'] == 'MacOS') |
                            (proj_df['OS'] == 'Windows')]

    ### Dist

    sub_df_dist = proj_df.loc[((proj_df['OS'] == 'Linux-Xenial') &
                               (proj_df['Python'] == '3.7') &
                               (proj_df['Hardware'] == 'amd64')) |
                              (proj_df['OS'] == 'Linux-Bionic') |
                              (proj_df['OS'] == 'Linux-Focal')]

    ### Hardware

    sub_df_hw = proj_df.loc[((proj_df['OS'] == 'Linux-Xenial') &
                             (proj_df['Python'] == '3.7') &
                             (proj_df['Hardware'] == 'amd64')) |
                            (proj_df['Hardware'] == 'arm64-gravitation2') |
                            (proj_df['Hardware'] == 'arm64')]

    ### Python Versions

    sub_df_py = proj_df.loc[((proj_df['OS'] == 'Linux-Xenial') &
                             (proj_df['Python'] == '3.7') &
                             (proj_df['Hardware'] == 'amd64')) |
                            (proj_df['OS'] == 'Linux-Xenial') &
                            (proj_df['Python'] == '3.8') &
                            (proj_df['Hardware'] == 'amd64') |
                            (proj_df['OS'] == 'Linux-Xenial') &
                            (proj_df['Python'] == '3.6') &
                            (proj_df['Hardware'] == 'amd64')]

    return [sub_df_os, sub_df_dist, sub_df_hw, sub_df_py]


def perform_stat_analysis(proj_df):
    combined_model = ols("Score ~ C(OS) + C(Hardware) + C(Python)", proj_df).fit()

    sub_df_os, sub_df_dist, sub_df_hw, sub_df_py = create_sub_dfs(proj_df)

    os_model = ols("Score ~ C(OS)", sub_df_os).fit()

    dist_model = ols("Score ~ C(OS)", sub_df_dist).fit()

    hw_model = ols("Score ~ C(Hardware)", sub_df_hw).fit()

    py_model = ols("Score ~ C(Python)", sub_df_py).fit()

    return combined_model


@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun

    return df.to_csv().encode('utf-8')


def main():
    sample_data_path = os.path.realpath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'sample_processed_data', 'sample.json.gz'))
    print(sample_data_path)
    df = pd.read_json(sample_data_path, lines=True, compression='gzip')

    df['Python'] = df['Python'].astype(str)

    proj_list = df['Project'].unique().tolist()

    with st.sidebar:
        # create a selectbox option to select a project
        project = st.selectbox('Choose a Project', proj_list)

    proj_df = df.loc[df['Project'] == project]

    st.write(f"Raw data for project {project}")
    st.dataframe(proj_df.reset_index(), use_container_width=True, hide_index=True)

    st.download_button(label="Download data as CSV", data=convert_df(proj_df), file_name=f'{project}_df.csv',
                       mime='text/csv')

    st.write(f"Distribution of scores for different configuration variables:\n")
    # generate boxplot
    fig = plt.figure(figsize=(10, 10))
    fig = make_boxplot(create_sub_dfs(proj_df), project, fig)
    st.pyplot(fig)

    combined_model = perform_stat_analysis(proj_df)

    st.write(combined_model.summary())
    st.write(anova_lm(combined_model))


if __name__ == '__main__':
    main()
