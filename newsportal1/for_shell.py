from portal.models import *
# не знаю как запустить скрипт, кроме как в шелл
# нашел только лучшего автора, а не юзера (просто некогда искать по юзерам)



au_best = Author.objects.order_by('-rating')[0]
print(au_best.user.username)
post_best = au_best.post_set.all().order_by('-rating')[0]
print('автор: ',post_best.author.user.username)
print(f'дата: {post_best.date}\nзаголовок: {post_best.header}\nрейтинг: {post_best.rating}\nпревью: {post_best.preview()}')
for i in post_best.comment_set.all():
    print(i.date,i.user.username,i.rating,i.comment)