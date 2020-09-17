'''
This script connects to College Results Online's website and uses  Beautiful Soup to scrape
data from more than 1,600 public and private 4-year univerisities in the US. The data is then
put into a dataframe and cleaned.
'''

from bs4 import BeautifulSoup
import requests
import pandas as pd

def str_to_int(string):
    '''
    A helper function to turn a string to an integer

    Parameters
    ----------
    string : A string of text.

    Returns
    -------
    A floating point number if the text is a number and None otherwise.
    '''
    try:
        return float(string)
    except (IndexError, ValueError):
        return None

def get_school_id_links():
    '''
    A helper function that loads in a csv file with universities and their unique
    links in order to webscrape data about them.

    Returns
    -------
    A list of links to use and a college_df with the name of the university.
    '''
    # Load in csv with unviersities and IPEDS ID
    college_df = pd.read_csv("../Data/4-Year-Public-and-Private-Universities-and-IPEDS-IDs.csv")

    # Convert ipeds_id column to string
    college_df.ipeds_id = college_df.ipeds_id.apply(str)

    # Saves the ID links
    links_to_follow = college_df.ipeds_id

    return links_to_follow, college_df

def get_college_dict(link):
    '''
    Creates a dictionary of the categories of scraped data for each university

    Parameters
    ----------
    id_link : The unique part of the link for one university.

    Returns
    -------
    A dictionary of scraped data for each of the univerisities.
    '''
    #Develop base URL
    base_url = "http://www.collegeresults.org/collegeprofile.aspx?institutionid="

    #Create full URL to scrape
    url = base_url + link

    #Request HTML and parse
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, "lxml")

    headers = ["ipeds_id", "college_name", "state", "size_undergrads", "percent_admitted",
               "in_state_tuition", "out_state_tuition", "sector", "average_gpa",
               "percent_part_time", "admission_test", "median_sat_verbal", "median_sat_math",
               "median_act_composite", "percent_underrep_minority", "pell_percent",
               "retention_rate", "four_year_grad_rate", "five_year_grad_rate", "six_year_grad_rate"]

    #ipeds_id
    ipeds_id = link

    # Name of college
    college_name = soup.find('h2').text

    # State
    state = soup.find_all(class_='data')[3].text

    # Size of undergrads
    raw_size_undergrads = soup.find_all(class_='data')[13].text.replace(",", "")
    size_undergrads = str_to_int(raw_size_undergrads)

    # Percent Admitted
    raw_percent_admitted = soup.find_all(class_='data')[26].text[:-1]
    percent_admitted = str_to_int(raw_percent_admitted)

    # In-State Tuition and Fees
    raw_in_state_tuition = soup.find_all(class_='data')[27].text[1:].replace(",", "")
    in_state_tuition = str_to_int(raw_in_state_tuition)

    # Out-of-State Tuition and Fees
    raw_out_state_tuition = soup.find_all(class_='data')[28].text[1:].replace(",", "")
    out_state_tuition = str_to_int(raw_out_state_tuition)

    # Sector (public or private)
    sector = soup.find_all(class_='data')[11].text

    # Average High School GPA Among College Freshmen
    raw_average_gpa = soup.find_all(class_='data')[19].text
    average_gpa = str_to_int(raw_average_gpa)

    # % Part time
    raw_percent_part_time = soup.find_all(class_='data')[49].text[:-1]
    percent_part_time = str_to_int(raw_percent_part_time)

    # Admission Test Scores Policy
    admission_test = soup.find_all(class_='data')[20].text

    # Median SAT Verbal
    raw_median_sat_verbal = soup.find_all(class_='data')[21].text[:3]
    median_sat_verbal = str_to_int(raw_median_sat_verbal)

    # Median SAT Math
    raw_median_sat_math = soup.find_all(class_='data')[22].text[:3]
    median_sat_math = str_to_int(raw_median_sat_math)

    # Median ACT Composite
    raw_median_act_composite = soup.find_all(class_='data')[24].text[:4]
    median_act_composite = str_to_int(raw_median_act_composite)

    # % Underrepresented minority
    raw_percent_underrep_minority = soup.find_all(class_='data')[36].text[:-1]
    percent_underrep_minority = str_to_int(raw_percent_underrep_minority)

    # Percent Pell grants
    raw_pell_percent = soup.find_all(class_='data')[35].text[:-1]
    pell_percent = str_to_int(raw_pell_percent)

    #First-year retention rate
    raw_retention_rate = soup.find_all(class_='data')[6].text[:-1]
    retention_rate = str_to_int(raw_retention_rate)

    # Four-year graduation rate
    raw_four_year_grad_rate = soup.find_all(class_='data')[7].text[:-1]
    four_year_grad_rate = str_to_int(raw_four_year_grad_rate)

    # Five-year graduation rate
    raw_five_year_grad_rate = soup.find_all(class_='data')[8].text[:-1]
    five_year_grad_rate = str_to_int(raw_five_year_grad_rate)

    # Six-year graduation rate
    raw_six_year_grad_rate = soup.find_all(class_='data')[9].text[:-1]
    six_year_grad_rate = str_to_int(raw_six_year_grad_rate)

    college_dict = dict(zip(headers, [ipeds_id, college_name, state, size_undergrads,
                                      percent_admitted, in_state_tuition, out_state_tuition,
                                      sector, average_gpa, percent_part_time, admission_test,
                                      median_sat_verbal, median_sat_math, median_act_composite,
                                      percent_underrep_minority, pell_percent, retention_rate,
                                      four_year_grad_rate, five_year_grad_rate,
                                      six_year_grad_rate]))

    return college_dict

def scrape_college_results_online(links_to_follow, college_df):
    '''
    Returns a dataframe with information scraped from College Results Online.

    Parameters
    ----------
    links_to_follow : The list of unique parts of the links for the univerisities.
    college_df : A dataframe with the names of univerisities and their id_links

    Returns
    -------
    A dataframe containing the information for univerisities.
    '''
    college_id_list = []

    for link in links_to_follow:
        try:
            college_id_list.append(get_college_dict(link))
        except NameError:
            continue

    college_page_info = pd.DataFrame(college_id_list)
    college_page_info.set_index('ipeds_id', inplace=True)

    # Reset the index for the college-df
    college_df.set_index('ipeds_id', inplace=True)

    # Merge the 2 dataframes
    college_df = college_df.merge(college_page_info, left_index=True, right_index=True)

    # Reset the index of the dataframe
    college_df = college_df.reset_index()

    return college_df

def clean_college_dataframe(college_df):
    '''
    This function cleans the college_df dataframe by removing duplicate columns, duplicate
    rows, and dropping rows with NaN values in certain columns.

    Parameters
    ----------
    college_df : The college dataframe.

    Returns
    -------
    college_df : A cleaner version of college_df.
    '''
    # Convert ipeds_id column to float
    college_df.ipeds_id = college_df.ipeds_id.apply(float)

    # Drop college name column (duplicate column)
    college_df = college_df.drop(columns=["college_name"])

    # Drop sector = for-profit (don't want these included)
    college_df.drop(college_df[college_df['sector'] == "Private for-profit"].index, inplace=True)

    # Drop sector = - (found these all to be for-profit)
    college_df.drop(college_df[college_df['sector'] == "-"].index, inplace=True)

    # Drop specific columns with missing values
    college_df = college_df.dropna(subset=['in_state_tuition', 'out_state_tuition', 'pell_percent',
                                           'percent_admitted', 'retention_rate', 'admission_test',
                                           'four_year_grad_rate', 'five_year_grad_rate',
                                           'six_year_grad_rate'])
    return college_df

def clean_missing_gpa(college_df):
    '''
    This function cleans the college_df dataframe by filling in missing values of the GPA
    column with averages based on the number of applicants the university admits.

    Parameters
    ----------
    college_df : The college dataframe.

    Returns
    -------
    college_df : A cleaner version of college_df.
    '''
    # Percent admitted at 20% or below
    select20 = college_df["percent_admitted"] <= 20
    college_df[select20] = college_df[select20].fillna(college_df.average_gpa.mean())

    # Percent admitted at between 21-40%
    select21_40 = ((college_df["percent_admitted"] > 20) & (college_df.percent_admitted <= 40))
    college_df[select21_40] = college_df[select21_40].fillna(college_df.average_gpa.mean())

    # Percent admitted at between 41-60%
    select41_60 = ((college_df["percent_admitted"] > 40) & (college_df.percent_admitted <= 60))
    college_df[select41_60] = college_df[select41_60].fillna(college_df.average_gpa.mean())

    select61_80 = ((college_df["percent_admitted"] > 60) & (college_df.percent_admitted <= 80))
    college_df[select61_80] = college_df[select61_80].fillna(college_df.average_gpa.mean())

    # Percent admitted at between 81-99%
    select81_99 = ((college_df["percent_admitted"] > 80) & (college_df.percent_admitted < 100))
    college_df[select81_99] = college_df[select81_99].fillna(college_df.average_gpa.mean())

    # Percent admitted = 100%
    select100 = college_df["percent_admitted"] == 100
    college_df[select100] = college_df[select100].fillna(college_df.average_gpa.mean())

    return college_df

def clean_missing_sat_reading(college_df):
    '''
    This function cleans the college_df dataframe by filling in missing values of the SAT
    Reading column with averages based on the number of applicants the university admits.

    Parameters
    ----------
    college_df : The college dataframe.

    Returns
    -------
    college_df : A cleaner version of college_df.
    '''
    # Percent admitted at 20% or below
    sat_verbal_select20 = college_df["percent_admitted"] <= 20
    college_df[sat_verbal_select20] = college_df[sat_verbal_select20].fillna(
        college_df.median_sat_verbal.mean())

    # Percent admitted at between 21-40%
    sat_verbal_select21_40 = ((college_df["percent_admitted"] > 20) &
                              (college_df.percent_admitted <= 40))
    college_df[sat_verbal_select21_40] = college_df[sat_verbal_select21_40].fillna(
        college_df.median_sat_verbal.mean())

    # Percent admitted at between 41-60%
    sat_verbal_select41_60 = ((college_df["percent_admitted"] > 40) &
                              (college_df.percent_admitted <= 60))
    college_df[sat_verbal_select41_60] = college_df[sat_verbal_select41_60].fillna(
        college_df.median_sat_verbal.mean())

    # Percent admitted at between 61-80%
    sat_verbal_select61_80 = ((college_df["percent_admitted"] > 60) &
                              (college_df.percent_admitted <= 80))
    college_df[sat_verbal_select61_80] = college_df[sat_verbal_select61_80].fillna(
        college_df.median_sat_verbal.mean())

    # Percent admitted at between 81-99%
    sat_verbal_select81_99 = ((college_df["percent_admitted"] > 80) &
                              (college_df.percent_admitted < 100))
    college_df[sat_verbal_select81_99] = college_df[sat_verbal_select81_99].fillna(
        college_df.median_sat_verbal.mean())

    # Percent admitted = 100%
    sat_verbal_select100 = college_df["percent_admitted"] == 100
    college_df[sat_verbal_select100] = college_df[sat_verbal_select100].fillna(
        college_df.median_sat_verbal.mean())

    return college_df

def clean_missing_sat_math(college_df):
    '''
    This function cleans the college_df dataframe by filling in missing values of the SAT
    Math column with averages based on the number of applicants the university admits.

    Parameters
    ----------
    college_df : The college dataframe.

    Returns
    -------
    college_df : A cleaner version of college_df.
    '''
    # Percent admitted at 20% or below
    sat_math_select20 = college_df["percent_admitted"] <= 20
    college_df[sat_math_select20] = college_df[sat_math_select20].fillna(
        college_df.median_sat_math.mean())

    # Percent admitted at between 21-40%
    sat_math_select21_40 = ((college_df["percent_admitted"] > 20) &
                            (college_df.percent_admitted <= 40))
    college_df[sat_math_select21_40] = college_df[sat_math_select21_40].fillna(
        college_df.median_sat_math.mean())

    # Percent admitted at between 41-60%
    sat_math_select41_60 = ((college_df["percent_admitted"] > 40) &
                            (college_df.percent_admitted <= 60))
    college_df[sat_math_select41_60] = college_df[sat_math_select41_60].fillna(
        college_df.median_sat_math.mean())

    # Percent admitted at between 61-80%
    sat_math_select61_80 = ((college_df["percent_admitted"] > 60) &
                            (college_df.percent_admitted <= 80))
    college_df[sat_math_select61_80] = college_df[sat_math_select61_80].fillna(
        college_df.median_sat_math.mean())

    # Percent admitted at between 81-99%
    sat_math_select81_99 = ((college_df["percent_admitted"] > 80) &
                            (college_df.percent_admitted < 100))
    college_df[sat_math_select81_99] = college_df[sat_math_select81_99].fillna(
        college_df.median_sat_math.mean())

    # Percent admitted = 100%
    sat_math_select100 = college_df["percent_admitted"] == 100
    college_df[sat_math_select100] = college_df[sat_math_select100].fillna(
        college_df.median_sat_math.mean())

    return college_df

def clean_missing_act(college_df):
    '''
    This function cleans the college_df dataframe by filling in missing values of the ACT
    column with averages based on the number of applicants the university admits.

    Parameters
    ----------
    college_df : The college dataframe.

    Returns
    -------
    college_df : A cleaner version of college_df.
    '''
    # Percent admitted at 20% or below
    act_select20 = college_df["percent_admitted"] <= 20
    college_df[act_select20] = college_df[act_select20].fillna(
        college_df.median_act_composite.mean())

    # Percent admitted at between 21-40%
    act_select21_40 = ((college_df["percent_admitted"] > 20) &
                       (college_df.percent_admitted <= 40))
    college_df[act_select21_40] = college_df[act_select21_40].fillna(
        college_df.median_act_composite.mean())

    # Percent admitted at between 41-60%
    act_select41_60 = ((college_df["percent_admitted"] > 40) &
                       (college_df.percent_admitted <= 60))
    college_df[act_select41_60] = college_df[act_select41_60].fillna(
        college_df.median_act_composite.mean())

    # Percent admitted at between 61-80%
    act_select61_80 = ((college_df["percent_admitted"] > 60) &
                       (college_df.percent_admitted <= 80))
    college_df[act_select61_80] = college_df[act_select61_80].fillna(
        college_df.median_act_composite.mean())

    # Percent admitted at between 81-99%
    act_select81_99 = ((college_df["percent_admitted"] > 80) &
                       (college_df.percent_admitted < 100))
    college_df[act_select81_99] = college_df[act_select81_99].fillna(
        college_df.median_act_composite.mean())

    # Percent admitted = 100%
    act_select100 = college_df["percent_admitted"] == 100
    college_df[act_select100] = college_df[act_select100].fillna(
        college_df.median_act_composite.mean())

    return college_df

def final_data_cleaning(college_df):
    '''
    This function cleans the college_df dataframe by adding dummy variables and then drops
    four- and six-year graduation rates. The final dataframe is saved as a csv file.

    Parameters
    ----------
    college_df : The college dataframe.

    Returns
    -------
    five_college_df : A final cleaned version of the college dataframe with only five-year
    graduation rates that has been saved to a csv file.
    '''
    # Create dummy variables
    college_df = pd.get_dummies(college_df, prefix=['sector', 'admission_test'],
                                columns=['sector', 'admission_test'], drop_first=True)

    # Convert dummy variable types to int
    college_df.sector_Public = college_df.sector_Public.apply(int)
    college_df["admission_test_Considered but not required"] = college_df[
                "admission_test_Considered but not required"].apply(int)
    college_df["admission_test_Neither required nor recommended"] = college_df[
                "admission_test_Neither required nor recommended"].apply(int)
    college_df["admission_test_Recommended"] = college_df["admission_test_Recommended"].apply(int)
    college_df["admission_test_Required"] = college_df["admission_test_Required"].apply(int)

    # Create a data frame with just 5 year graduation rate as predictor
    five_college_df = college_df.drop(['four_year_grad_rate', 'six_year_grad_rate'], axis=1)

    # Save dataframe to csv files
    five_college_df.to_csv(r'five_college_df.csv', index=False)

def main():
    '''
    Calls internal functions to the script to scrape data from College Results Online website,
    then creates dataframe with the data, and finally cleans the data.
    '''

    # Call internal functions to this script
    links_to_follow, college_df = get_school_id_links()
    college_df = scrape_college_results_online(links_to_follow, college_df)
    college_df = clean_college_dataframe(college_df)
    college_df = clean_missing_gpa(college_df)
    college_df = clean_missing_sat_reading(college_df)
    college_df = clean_missing_sat_math(college_df)
    college_df = clean_missing_act(college_df)
    final_data_cleaning(college_df)

main()
