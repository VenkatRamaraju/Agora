drop table if exists ticker_info;

create table ticker_info (
    Ticker text primary key,
    Company_name text not null,
    Analyst_rating text not null,
    Headlines_polarity float not null,
    Conversations_polarity float not null
);

drop table if exists ticker_headlines;

create table ticker_headlines (
    Headline text primary key,
    Ticker text foreign key (Ticker) references ticker_info (Ticker)
);