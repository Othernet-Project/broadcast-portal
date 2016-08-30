<%def name="content_item(item)">
    <p class="item-info item-name">
        <span class="icon icon-file"></span>
        ${item.filename} 
    </p>
    <p class="item-info item-attribution">
        ${_('Uploaded by {username} {timeago}').format(username=item.username, timeago=th.human_time(item.created))}
    </p>
    <p class="item-info item-download">
        <a class="button button-small" href="${url('queue:download', item_id=item.id)}">
            <span class="icon icon-download"></span>
            <span class="invisible-label">${_('download')}</span>
            <span class="supplementary-info">${h.hsize(item.size)}</span>
        </a> 
    </p>
    <form class="vote-form" action="${url('queue:vote', item_id=item.id)}" method="POST">
        <input type="hidden" name="next" value="${request.fullpath}">
        <button class="vote-icon vote-up" type="submit" name="upvote" value="yes"${' disabled' if item.user_vote == 1 else ''}>
            <span class="icon icon-expand-up"></span>
            <span class="invisible-label">${_('upvote')}</span>
        </button>
        <span class="vote-count">${item.votes}</span>
        <button class="vote-icon vote-down" type="submit" name="upvote" value="no"${' disabled' if item.user_vote == -1 else ''}>
            <span class="invisible-label">${_('downvote')}</span>
            <span class="icon icon-expand-down"></span>
        </button>
    </form>
</%def>
