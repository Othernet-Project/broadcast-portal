<%def name="content_item(item)">
    <p class="item-info item-name">
        ${item.path} <a href="${url('queue:download', item_id=item.id)}">${_('download')}</a>
    </p>
    <p class="item-info item-attribution">
        ${_('Uploaded by {username} {timeago}').format(username=item.username, timeago=th.human_time(item.created))}
    </p>
    <form class="vote-form" action="${url('queue:vote', item_id=item.id)}" method="POST">
        <input type="hidden" name="next" value="${request.fullpath}">
        <button class="vote-icon vote-up" type="submit" name="upvote" value="yes">${_('upvote')}</button>
        ${item.votes}
        <button class="vote-icon vote-down" type="submit" name="upvote" value="no">${_('downvote')}</button>
    </form>
</%def>