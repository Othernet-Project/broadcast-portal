<%inherit file='base.tpl'/>
<%namespace name="item_list" file="_item_list.tpl"/>

<%block name="main">
    <div class="bin-heading">
        <h1 class="title">${_("Daily Bin")}</h1>
        <div class="bin-info-display">
            <%
               tsecs = bin.time_left.total_seconds()
               hours, remainder = divmod(tsecs, 3600)
               minutes, seconds = divmod(remainder, 60)
               broadcast_in = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            %>
            <span class="line">${_("Current bin size: {size} / {usage}%".format(size=h.hsize(bin.size), usage=round(bin.usage, 2)))}</span>
            <br />
            <span class="line">${_("Broadcasting in: {time}".format(time=broadcast_in))}</span>
        </div>
        <span class="bin-usage-bar light">
            <span class="bin-usage-bar-indicator" style="width: ${bin.usage}%"></span>
        </span>
    </div>

    <div class="bin">
        <p class="handles">
            <a class="handle ${ACCEPTED_QUEUE} ${'active' if queue_type == ACCEPTED_QUEUE else ''}" href="${url('queue_list', type=ACCEPTED_QUEUE)}" data-target="${ACCEPTED_QUEUE}">${_("Accepted")}</a>
            <a class="handle ${REVIEW_QUEUE} ${'active' if queue_type == REVIEW_QUEUE else ''}" href="${url('queue_list', type=REVIEW_QUEUE)}" data-target="${REVIEW_QUEUE}">${_("Review")}</a>
        </p>

        ${h.form('get', _class="search", action=url('queue_list'))}
            ${h.HIDDEN('type', queue_type)}
            ${h.vinput('query', locals(), _type="text", _class="search-query", _placeholder=_("Search"))}
            <button type="submit"><span class="icon">${_('Search')}</span></button>
        </form>

        <div class="items ${queue_type}" data-source="${queue_type}">
            ${item_list.body()}
        </div>

        <div class="items ${hidden_queue_type} hidden" data-source="${hidden_queue_type}"></div>
    </div>
</%block>

<%block name="extra_body">
    <script type="text/template" id="queueLoadError">
        ${_('Queue loading failed. Please try again in a few seconds.')}
    </script>
    <script type="text/template" id="queueModifyError">
        ${_('We were unable to modify the queue. Please try again in a few seconds.')}
    </script>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/queue']}"></script>
</%block>
