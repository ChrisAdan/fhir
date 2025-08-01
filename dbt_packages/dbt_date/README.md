<div align="center">
	<img src="https://img.shields.io/github/v/tag/godatadriven/dbt-date?logo=github">
  <img src="https://img.shields.io/badge/dbt--core-%3E=1.6%20%3C=1.9.x-orange?logo=dbt">
	<img src="https://img.shields.io/badge/license-Apache--2.0-ff69b4?style=plastic">
  <img src="https://img.shields.io/github/last-commit/godatadriven/dbt-date/main">
</div>

# dbt-date

`dbt-date` is an extension package for [**dbt**](https://github.com/dbt-labs/dbt) to handle common date logic and calendar functionality.

Development of `dbt-date` is supported by [Xebia Data](https://xebia.com/digital-transformation/data-and-ai/) (formerly known as GoDataDriven):

<div class="row">
  <div class="column" align="center">
    <img src="https://github.com/godatadriven/dbt-date/blob/8fd16fb70af3ff9fffe14439eb4a83cf1d10c03f/images/xebia-logo-large-transparent.png" href="https://xebia.com/digital-transformation/data-and-ai/" media="(prefers-color-scheme: dark)" alt="Xebia logo" title="Xebia" style="width:40%; padding: 0px 10px 0px 0px">
  </div>
</div>

## Install

Include in `packages.yml`

```yaml
packages:
  - package: godatadriven/dbt_date
    version: [">=0.11.0", "<0.12.0"]
    # <see https://github.com/godatadriven/dbt-date/tags> for the latest version tag
```

## Supported Adapters

| Adapter    | Full Support       | Partial Support    |
| ---------- | ------------------ | ------------------ |
| BigQuery   | :white_check_mark: |                    |
| Databricks | :white_check_mark: |                    |
| DuckDB     | :white_check_mark: |                    |
| Postgres   | :white_check_mark: |                    |
| Spark      | :white_check_mark: |                    |
| Trino      | :white_check_mark: |                    |
| Snowflake  |                    | :white_check_mark: |

- **Full Support**: Macros are tested against this adapter on every pull request and merge to `main`.
- **Partial Support**: Macros are not tested against this adapter on every pull request and merge to `main`. Support is provided, please create an [issue](https://github.com/godatadriven/dbt-date/issues).

## Variables

The following variables need to be defined in your `dbt_project.yml` file:

```yaml
vars:
  "dbt_date:time_zone": "America/Los_Angeles"
```

You may specify [any valid timezone string](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) in place of `America/Los_Angeles`.
For example, use `America/New_York` for East Coast Time.

## Available Macros

### Date Dimension

- [get_base_dates](#get_base_datesstart_datenone-end_datenone-n_datepartsnone-datepartday)
- [get_date_dimension](#get_date_dimensionstart_date-end_date)

### Calendar Date

- [convert_timezone](#convert_timezone-column-target_tznone-source_tznone)
- [date_part](#date_partdatepart-date)
- [day_name](#day_namedate-shorttrue-languagedefault)
- [day_of_month](#day_of_monthdate)
- [day_of_week](#day_of_weekdate-isoweektrue)
- [day_of_year](#day_of_yeardate)
- [from_unixtimestamp](#from_unixtimestampepochs-formatseconds)
- [iso_week_end](#iso_week_enddatenone-tznone)
- [iso_week_of_year](#iso_week_of_yeardatenone-tznone)
- [iso_year_week](#iso_year_weekdate)
- [iso_week_start](#iso_week_startdatenone-tznone)
- [last_month_name](#last_month_nameshorttrue-tznone)
- [last_month_number](#last_month_numbertznone)
- [last_month](#last_monthtznone)
- [last_week](#last_weektznone)
- [month_name](#month_namedate-shorttrue-tznone-languagedefault)
- [n_days_ago](#n_days_agon-datenone-tznone)
- [n_days_away](#n_days_awayn-datenone-tznone)
- [n_months_ago](#n_months_agon-tznone)
- [n_months_away](#n_months_awayn-tznone)
- [n_weeks_ago](#n_weeks_agon-tznone)
- [n_weeks_away](#n_weeks_awayn-tznone)
- [next_month_name](#next_month_nameshorttrue-tznone)
- [next_month_number](#next_month_numbertznone)
- [next_month](#next_monthtznone)
- [next_week](#next_weektznone)
- [now](#nowtznone)
- [periods_since](#periods_sincedate_col-period_nameday-tznone)
- [round_timestamp](#round_timestamptimestamp)
- [to_unixtimestamp](#to_unixtimestamptimestamp)
- [today](#todaytznone)
- [tomorrow](#tomorrowdatenone-tznone)
- [week_end](#week_enddatenone-tznone)
- [week_of_year](#week_of_yeardatenone-tznone)
- [week_start](#week_startdatenone-tznone)
- [yesterday](#yesterdaydatenone-tznone)

## Fiscal Date

- [get_fiscal_periods](#get_fiscal_periodsdates-year_end_month-week_start_day-shift_year1)

## Utils

- [date](#dateyear-month-day)
- [datetime](#datetimeyear-month-day-hour0-minute0-second0-microsecond0-tznone)

## Documentation

### [get_base_dates](macros/get_base_dates.sql)(`start_date=None, end_date=None, n_dateparts=None, datepart="day"`)

A wrapper around [`dbt_utils.date_spine`](https://github.com/dbt-labs/dbt-utils#date_spine-source) that allows you to specify either `start_date` and `end_date` for your date spine, or specify a number of periods (`n_dateparts`) in the past from today.

Usage to build a daily date dimension for the years 2015 to 2022:

```sql
{{ dbt_date.get_base_dates(start_date="2015-01-01", end_date="2023-01-01") }}
```

or to build a daily date dimension for the last 3 years:

```sql
{{ dbt_date.get_base_dates(n_dateparts=365*3, datepart="day") }}
```

### [get_date_dimension](macros/get_date_dimension.sql)(`start_date, end_date`)

Returns a query to build date dimension from/to specified dates, including a number of useful columns based on each date.
See the [example model](integration_tests/models/dim_date.sql) for details.

Usage:

```sql
{{ dbt_date.get_date_dimension("2015-01-01", "2022-12-31") }}
```

### Fiscal Periods

### [get_fiscal_periods](macros/fiscal_date/get_fiscal_periods.sql)(`dates, year_end_month, week_start_day, shift_year=1`)

Returns a query to build a fiscal period calendar based on the 4-5-4 week retail period concept.
See the [example model](integration_tests/models/dim_date_fiscal.sql) for details and this [blog post](https://calogica.com/sql/dbt/2018/11/15/retail-calendar-in-sql.html) for more context on custom business calendars.

Usage:

```sql
{{ dbt_date.get_fiscal_periods(ref("dates"), year_end_month, week_start_day) }}
```

Note: the first parameter expects a dbt `ref` variable, i.e. a reference to a model containing the necessary date dimension attributes, which can be generated via the `get_date_dimension` macro (see above).

### Date

### [convert_timezone](macros/calendar_date/convert_timezone.sql)( `column, target_tz=None, source_tz=None`)

Cross-database implemention of convert_timezone function.

Usage:

```sql
{{ dbt_date.convert_timezone("my_column") }}
```

or, specify a target timezone:

```sql
{{ dbt_date.convert_timezone("my_column", "America/New_York") }}
```

or, also specify a source timezone:

```sql
{{ dbt_date.convert_timezone("my_column", "America/New_York", "UTC") }}
```

Using named parameters, we can also specify the source only and rely on the configuration parameter for the target:

```sql
{{ dbt_date.convert_timezone("my_column", source_tz="UTC") }}
```

### [date_part](macros/calendar_date/date_part.sql)(`datepart, date`)

Extracts date parts from date.

Usage:

```sql
{{ dbt_date.date_part("dayofweek", "date_col") }} as day_of_week
```

### [day_name](macros/calendar_date/day_name.sql)(`date, short=True, language="default"`)

Extracts name of weekday from date. For `language=default` this will return the name depending on the language set in the database. To get weekday names in a specific language use the two-letter language abbreviation of a supported language (en, nl, de, fr, es, it, pt, pl, da, sv, tr, cs, fi) or overwrite the `get_localized_datepart_names` macro with your own language of choice.

Usage:

```sql
{{ dbt_date.day_name("date_col") }} as day_of_week_short_name
```

```sql
{{ dbt_date.day_name("date_col", short=true) }} as day_of_week_short_name
```

```sql
{{ dbt_date.day_name("date_col", short=false, language="es") }} as day_of_week_long_name_localized
```

### [day_of_month](macros/calendar_date/day_of_month.sql)(`date`)

Extracts day of the month from a date (e.g. `2022-03-06` --> `6`).

Usage:

```sql
{{ dbt_date.day_of_month("date_col") }} as day_of_month
```

### [day_of_week](macros/calendar_date/day_of_week.sql)(`date, isoweek=true`)

Extracts day of the week _number_ from a date, starting with **1**.
By default, uses `isoweek=True`, i.e. assumes week starts on _Monday_.

Usage:

```sql
{{ dbt_date.day_of_week("'2022-03-06'") }} as day_of_week_iso
```

returns: **7** (Sunday is the _last_ day of the ISO week)

```sql
{{ dbt_date.day_of_week("'2022-03-06'", isoweek=False) }} as day_of_week
```

returns: **1** (Sunday is the _first_ day of the non-ISO week)

### [day_of_year](macros/calendar_date/day_of_year.sql)(`date`)

Extracts day of the year from a date (e.g. `2022-02-02` --> `33`).

Usage:

```sql
{{ dbt_date.day_of_year("date_col") }} as day_of_year
```

or

```sql
{{ dbt_date.day_of_year("'2022-02-02'") }} as day_of_year
```

returns: **33**

### [from_unixtimestamp](macros/calendar_date/from_unixtimestamp.sql)(`epochs, format="seconds"`)

Converts an `epoch` into a timestamp. The default for `format` is `seconds`, which can overriden depending your data"s epoch format.

Usage:

```sql
{{ dbt_date.from_unixtimestamp("epoch_column") }} as timestamp_column
```

```sql
{{ dbt_date.from_unixtimestamp("epoch_column", format="milliseconds") }} as timestamp_column
```

See also: [to_unixtimestamp](#to_unixtimestamp)

### [iso_week_end](macros/calendar_date/iso_week_end.sql)(`date=None, tz=None`)

Computes the week ending date using ISO format, i.e. week starting **Monday** and ending **Sunday**.

Usage:

```sql
{{ dbt_date.iso_week_end("date_col") }} as iso_week_end_date
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.iso_week_end("date_col", tz="America/New_York") }} as iso_week_end_date
```

### [iso_week_of_year](macros/calendar_date/iso_week_of_year.sql)(`date=None, tz=None`)

Computes the week of the year using ISO format, i.e. week starting **Monday**.

Usage:

```sql
{{ dbt_date.iso_week_of_year("date_col") }} as iso_week_of_year
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.iso_week_of_year("date_col", tz="America/New_York") }} as iso_week_of_year
```

### [iso_year_week](macros/calendar_date/iso_year_week.sql)(`date`)

Computes the year-week combination in ISO-format, e.g. `2026-W01`. Combining year and week seperately will return incorrect results at the edges of the year as start and end dates of the week might fall in a different year. This macro calculates the correct year for the ISO week, e.g. December 31st can fall in week 01 of the next year.

### [iso_week_start](macros/calendar_date/iso_week_start.sql)(`date=None, tz=None`)

Computes the week starting date using ISO format, i.e. week starting **Monday**.

Usage:

```sql
{{ dbt_date.iso_week_start("date_col") }} as iso_week_start_date
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.iso_week_start("date_col", tz="America/New_York") }} as iso_week_start_date
```

### [last_month_name](macros/calendar_date/last_month_name.sql)(`short=True, tz=None`)

Extracts the name of the prior month from a date.

```sql
{{ dbt_date.last_month_name() }} as last_month_short_name
```

```sql
{{ dbt_date.last_month_name(short=true) }} as last_month_short_name
```

```sql
{{ dbt_date.last_month_name(short=false) }} as last_month_long_name
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.last_month_name(tz="America/New_York") }} as last_month_short_name
```

### [last_month_number](macros/calendar_date/last_month_number.sql)(`tz=None`)

Returns the number of the prior month.

```sql
{{ dbt_date.last_month_number() }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.last_month_number(tz="America/New_York") }}
```

### [last_month](macros/calendar_date/last_month.sql)(`tz=None`)

Returns the start date of the prior month.

```sql
{{ dbt_date.last_month() }} as last_month_start_date
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.last_month(tz="America/New_York") }} as last_month_start_date
```

### [last_week](macros/calendar_date/last_week.sql)(`tz=None`)

Convenience function to get the start date of last week (non-ISO)

Wraps:

```sql
{{ dbt_date.n_weeks_ago(1, tz) }}
```

Usage:

```sql
{{ dbt_date.last_week()) }} as last_week_start_date
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.last_week(tz="America/New_York)) }} as last_week_start_date
```

### [month_name](macros/calendar_date/month_name.sql)(`date, short=True, tz=None, language="default"`)

Extracts the name of the month from a date. For `language=default` this will return the name depending on the language set in the database. To get month names in a specific language use the two-letter language abbreviation of a supported language (en, nl, de, fr, es, it, pt, pl, da, sv, tr, cs, fi) or overwrite the `get_localized_datepart_names` macro with your own language of choice.

```sql
{{ dbt_date.month_name(date_col) }} as month_short_name
```

```sql
{{ dbt_date.month_name(date_col, short=true) }} as month_short_name
```

```sql
{{ dbt_date.month_name(date_col, short=false, language="nl") }} as month_long_name_localized
```

### [n_days_ago](macros/calendar_date/n_days_ago.sql)(`n, date=None, tz=None`)

Gets date _n_ days ago, based on local date.

Usage:

```sql
{{ dbt_date.n_days_ago(7) }}
```

Alternatively, you can specify a date column instead of defaulting the local date:

```sql
{{ dbt_date.n_days_ago(7, date="date_col") }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.n_days_ago(7, tz="America/New_York)) }}
```

### [n_days_away](macros/calendar_date/n_days_away.sql)(`n, date=None, tz=None`)

Gets date _n_ days away, based on local date.

Usage:

```sql
{{ dbt_date.n_days_away(7) }}
```

Alternatively, you can specify a date column instead of defaulting the local date:

```sql
{{ dbt_date.n_days_away(7, date="date_col") }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.n_days_away(7, tz="America/New_York)) }}
```

### [n_months_ago](macros/calendar_date/n_months_ago.sql)(`n, tz=None`)

Gets date _n_ months ago, based on local date.

Usage:

```sql
{{ dbt_date.n_months_ago(12) }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.n_months_ago(12, tz="America/New_York)) }}
```

### [n_months_away](macros/calendar_date/n_months_away.sql)(`n, tz=None`)

Gets date _n_ months away, based on local date.

Usage:

```sql
{{ dbt_date.n_months_ago(12) }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.n_months_away(12, tz="America/New_York)) }}
```

### [n_weeks_ago](macros/calendar_date/n_weeks_ago.sql)(`n, tz=None`)

Gets date _n_ weeks ago, based on local date.

Usage:

```sql
{{ dbt_date.n_weeks_ago(12) }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.n_weeks_ago(12, tz="America/New_York)) }}
```

### [n_weeks_away](macros/calendar_date/n_weeks_away.sql)(`n, tz=None`)

Gets date _n_ weeks away, based on local date.

Usage:

```sql
{{ dbt_date.n_weeks_away(12) }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.n_weeks_away(12, tz="America/New_York)) }}
```

### [next_month_name](macros/calendar_date/next_month_name.sql)(`short=True, tz=None`)

Extracts the name of the next month from a date.

```sql
{{ dbt_date.next_month_name() }} as next_month_short_name
```

```sql
{{ dbt_date.next_month_name(short=true) }} as next_month_short_name
```

```sql
{{ dbt_date.next_month_name(short=false) }} as next_month_long_name
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.next_month_name(tz="America/New_York") }} as next_month_short_name
```

### [next_month_number](macros/calendar_date/next_month_number.sql)(`tz=None`)

Returns the number of the next month.

```sql
{{ dbt_date.next_month_number() }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.next_month_number(tz="America/New_York") }}
```

### [next_month](macros/calendar_date/next_month.sql)(`tz=None`)

Returns the start date of the next month.

```sql
{{ dbt_date.next_month() }} as next_month_start_date
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.next_month(tz="America/New_York") }} as next_month_start_date
```

### [next_week](macros/calendar_date/next_week.sql)(`tz=None`)

Convenience function to get the start date of next week (non-ISO)

Wraps:

```sql
{{ dbt_date.n_weeks_away(1, tz) }}
```

Usage:

```sql
{{ dbt_date.next_week()) }} as next_week_start_date
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.next_week(tz="America/New_York") }}  as next_week_start_date
```

### [now](macros/calendar_date/now.sql)(`tz=None`)

Gets current timestamp based on local timezone (specified). Default is "America/Los_Angeles".

Usage:

```sql
{{ dbt_date.now() }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.now("America/New_York") }}
```

### [periods_since](macros/calendar_date/periods_since.sql)(`date_col, period_name='day', tz=None`)

Returns the number of periods since a specified date or to `now`.

Usage:

```sql
{{ dbt_date.periods_since("my_date_column", period_name="day") }}
```

or,

```sql
{{ dbt_date.periods_since("my_timestamp_column", period_name="minute") }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.periods_since("my_timestamp_column", period_name="minute", tz="UTC") }}
```

### [round_timestamp](macros/calendar_date/round_timestamp.sql)(`timestamp`)

Rounds the given timestamp or date to the nearest date (return type is `timestamp`).

```sql
select
{{ dbt_date.round_timestamp("timestamp_col") }} as nearest_date
...
```

A few examples:

```sql
{{ dbt_date.round_timestamp("'2022-02-05 18:45:15'")}}
-- results in 2022-02-06
```

```sql
{{ dbt_date.round_timestamp("'2022-02-05 11:45:15'")}}
-- results in 2022-02-05
```

```sql
{{ dbt_date.round_timestamp("'2022-02-05 12:00:00'")}}
-- results in 2022-02-06
```

```sql
{{ dbt_date.round_timestamp("'2022-02-05 00:00:00'")}}
-- results in 2022-02-05
```

### [to_unixtimestamp](macros/calendar_date/to_unixtimestamp.sql)(`timestamp`)

Gets Unix timestamp (epochs) based on provided timestamp.

Usage:

```sql
{{ dbt_date.to_unixtimestamp("my_timestamp_column") }}
```

```sql
{{ dbt_date.to_unixtimestamp(dbt_date.now()) }}
```

### [today](macros/calendar_date/today.sql)(`tz=None`)

Gets date based on local timezone.

Usage:

```sql
{{ dbt_date.today() }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.today("America/New_York") }}
```

### [tomorrow](macros/calendar_date/tomorrow.sql)(`date=None, tz=None`)

Gets tomorrow's date, based on local date.

Usage:

```sql
{{ dbt_date.tomorrow() }}
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.tomorrow(tz="America/New_York") }} as date_tomorrow
```

Alternatively, you can also override the anchor date from the default `today` to some other date:

```sql
{{ dbt_date.tomorrow(date="date_col", tz="America/New_York") }} as date_tomorrow
```

### [week_end](macros/calendar_date/week_end.sql)(`date=None, tz=None`)

Computes the week ending date using standard (US) format, i.e. week starting **Sunday**.

Usage:

If `date` is not specified, the date anchor defaults to `today`.

```sql
{{ dbt_date.week_end() }} as week_end_date
```

or specify a date (column):

```sql
{{ dbt_date.week_end("date_col") }} as week_end_date
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.week_end("date_col", tz="America/New_York") }} as week_end_date
```

### [week_of_year](macros/calendar_date/week_of_year.sql)(`date=None, tz=None`)

Computes the week of the year using standard (US) format, i.e. week starting **Sunday** and ending **Saturday**.

Usage:

If `date` is not specified, the date anchor defaults to `today`.

```sql
{{ dbt_date.week_of_year() }} as week_of_year
```

or specify a date (column):

```sql
{{ dbt_date.week_of_year("date_col") }} as week_of_year
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.week_of_year("date_col", tz="America/New_York") }} as week_of_year
```

### [week_start](macros/calendar_date/week_start.sql)(`date=None, tz=None`)

Computes the week starting date using standard (US) format, i.e. week starting **Sunday**.

Usage:

If `date` is not specified, the date anchor defaults to `today`.

```sql
{{ dbt_date.week_start() }} as week_start
```

or specify a date (column):

```sql
{{ dbt_date.week_start("date_col") }} as week_start
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.week_start("date_col", tz="America/New_York") }} as week_start
```

### [yesterday](macros/calendar_date/yesterday.sql)(`date=None, tz=None`)

Gets yesterday's date, based on local date.

Usage:

If `date` is not specified, the date anchor defaults to `today`.

```sql
{{ dbt_date.yesterday() }} as date_yesterday
```

or specify a date (column):

```sql
{{ dbt_date.yesterday("date_col") }} as date_yesterday
```

or, optionally, you can override the default timezone:

```sql
{{ dbt_date.yesterday(tz="America/New_York") }} as date_yesterday
```

### [date](macros/_utils/modules_datetime.sql)(`year`, `month`, `day`)

Reduces the boilerplate syntax required to produce a `date` object. This is not converted to a string to allow pythonic manipulation.

Usage:

```sql
{% set date_object = dbt_date.date(1997, 9, 29) %}
```

### [datetime](macros/_utils/modules_datetime.sql)(`year`, `month`, `day`, `hour=0`, `minute=0`, `second=0`, `microsecond=0`, `tz=None`)

Reduces the boilerplate syntax required to produce a `datetime` object. This is not converted to a string to allow pythonic manipulation.

Usage:

```sql
{% set datetime_object = dbt_date.datetime(1997, 9, 29, 6, 14) %}
```

or, optionally, you can override the default timezone:

```sql
{% set datetime_object = dbt_date.datetime(1997, 9, 29, 6, 14, tz='America/New_York') %}
```

## Contributing

This project contains integration tests for all macros in a separate `integration_tests` dbt project contained in this repo.

1. Set up your development environment:

   ```shell
   python -m venv .venv
   source .venv/bin/activate
   make setup
   ```

2. Copy `.env_example` to `.env` and fill in the necessary values. Set the environment variables:

   ```shell
   source .env
   ```

3. Run the integration tests:

   - To run all tests in parallel:

     ```shell
     tox -p all
     ```

   - To run all tests in series:

     ```shell
     tox
     ```

   - To run tests for a specific adapter:

     ```shell
     tox -e dbt_integration_<ADAPTER>
     ```

4. To debug on a specific adapters:

   ```shell
   dbt debug --target <ADAPTER>
   ```
