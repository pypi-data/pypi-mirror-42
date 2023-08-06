"""
Created on Sun Mar  3 23:25:36 2019

@author: Rohit Swami
"""

def get_continent(country_name):
    
    country_name = country_name.title()
    
    Africa = ['Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina', 'Burundi', 'Cameroon', 'Cape Verde',
              'Central African Republic', 'Chad', 'Comoros', 'Congo', 'Democratic Republic of Congo',
              'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana',
              'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia', 'Libya', 'Madagascar',
              'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger',
              'Nigeria', 'Rwanda', 'Sao Tome And Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia',
              'South Africa', 'South Sudan', 'Sudan', 'Swaziland', 'Tanzania', 'Togo', 'Tunisia', 'Uganda',
              'Zambia', 'Zimbabwe']
    
    Asia = ['Afghanistan', 'Bahrain', 'Bangladesh', 'Bhutan', 'Brunei', 'Burma', 'Myanmar', 'Cambodia',
            'China', 'East Timor', 'India', 'Indonesia', 'Iran', 'Iraq', 'Israel', 'Japan', 'Jordan',
            'Kazakhstan', 'North Korea', 'South Korea', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Lebanon',
            'Malaysia', 'Maldives', 'Mongolia', 'Nepal', 'Oman', 'Pakistan', 'Philippines', 'Qatar',
            'Russia', 'Russian Federation', 'Saudi Arabia', 'Singapore', 'Sri Lanka', 'Syria',
            'Tajikistan', 'Thailand', 'Turkey', 'Turkmenistan', 'United Arab Emirates', 'Uzbekistan',
            'Vietnam', 'Yemen']
    
    Europe = ['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan', 'Belarus', 'Belgium', 
              'Bosnia And Herzegovina', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark',
              'England', 'Estonia', 'Finland', 'France', 'Georgia', 'Germany', 'Greece', 'Hungary',
              'Iceland', 'Ireland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania', 'Luxembourg',
              'Macedonia', 'Malta', 'Moldova', 'Monaco', 'Montenegro', 'Netherlands', 'Norway', 
              'Poland', 'Portugal', 'Romania', 'San Marino', 'Scotland', 'Serbia', 'Slovakia',
              'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine', 'United Kingdom', 'Vatican City',
              'Wales']
    
    North_America = ['Antigua And Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada', 'Costa Rica', 'Cuba',
                     'Dominica', 'Dominican Republic', 'El Salvador', 'Grenada', 'Guatemala', 'Haiti',
                     'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Saint Kitts And Nevis',
                     'Saint Lucia', 'Saint Vincent And the Grenadines', 'Trinidad And Tobago', 'United States']
    
    Oceania = ['Australia', 'Fiji', 'Kiribati', 'Marshall Islands', 'Micronesia', 'Nauru', 'New Zealand',
               'Palau', 'Papua New', 'Guinea', 'Samoa', 'Solomon Islands', 'Tonga', 'Tuvalu', 'Vanuatu']
    
    South_America = ['Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Guyana', 'Paraguay',
                     'Peru', 'Suriname', 'Uruguay', 'Venezuela']
    
    
    if country_name in Africa:
        return 'Africa'
    elif country_name in Asia:
        return 'Asia'
    elif country_name in Europe:
        return 'Europe'
    elif country_name in North_America:
        return 'North America'
    elif country_name in Oceania:
        return 'Australia/Oceania'
    elif country_name in South_America:
        return 'South America'
    else:
        return "Can't Found "+country_name
    
