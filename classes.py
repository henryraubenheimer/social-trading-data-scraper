import peewee

db = peewee.MySQLDatabase(
    'etoro',
    user='devuser',
    password='389389mysql',
    host='localhost',
    port=3306
)


class investor(peewee.Model):

    name = peewee.TextField(primary_key=True)

    class Meta:

        database = db
        table_name = 'investor'


class investor_data(peewee.Model):

    investor = peewee.ForeignKeyField(investor, column_name='investor', backref='positions', on_delete='CASCADE', on_update='CASCADE')
    time = peewee.DateTimeField()
    profit = peewee.FloatField()
    risk = peewee.IntegerField()
    copiers = peewee.IntegerField()

    class Meta:

        database = db
        table_name = 'investor_data'
        primary_key = peewee.CompositeKey('investor', 'time')



class share(peewee.Model):

    ticker = peewee.TextField(primary_key=True)

    class Meta:

        database = db
        table_name = 'share'


class share_position(peewee.Model):

    investor = peewee.ForeignKeyField(investor, column_name='investor', backref='positions', on_delete='CASCADE', on_update='CASCADE')
    share = peewee.ForeignKeyField(share, column_name='share', backref='positions', on_delete='CASCADE', on_update='CASCADE')
    time = peewee.DateTimeField()
    direction = peewee.TextField()
    invested = peewee.FloatField()
    profit_loss = peewee.FloatField()
    value = peewee.FloatField()

    class Meta:

        database = db
        table_name = 'share_position'
        primary_key = peewee.CompositeKey('investor', 'share', 'time')


class transaction(peewee.Model):

    time = peewee.DateTimeField()
    investor = peewee.ForeignKeyField(investor, column_name='investor', backref='transactions', on_delete='CASCADE', on_update='CASCADE')
    share = peewee.ForeignKeyField(share, column_name='share', backref='transactions', on_delete='CASCADE', on_update='CASCADE')
    amount = peewee.FloatField()
    leverage = peewee.FloatField()
    open = peewee.FloatField()
    profit_loss = peewee.IntegerField()
    sl = peewee.FloatField()
    sale_date = peewee.DateTimeField()

    class Meta:

        database = db
        table_name = 'transaction'
        primary_key = peewee.CompositeKey('time', 'investor', 'share')