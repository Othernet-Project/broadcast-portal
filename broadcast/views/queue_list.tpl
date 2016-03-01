<%inherit file='base.tpl'/>
<%namespace name="queue_list" file="_queue_list.tpl"/>

<%block name="main">
    <div class="bin-status">
        <h1 class="title">${_("Daily Bin")}</h1>
        <div class="bin-info-display">
            <%
               tsecs = bin.time_left.total_seconds()
               hours, remainder = divmod(tsecs, 3600)
               minutes, seconds = divmod(remainder, 60)
               broadcast_in = '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
            %>
            <span class="line">${_("Current bin size: {size} / {usage}%".format(size=h.hsize(bin.size), usage=bin.usage))}</span>
            <br />
            <span class="line">${_("Broadcasting in: {time}".format(time=broadcast_in))}</span>
        </div>
        <span class="bin-usage-bar">
            <span class="bin-usage-bar-indicator" style="width: ${bin.usage}%"></span>
        </span>
    </div>

    <div class="bin-contents">
        <div class="handles">
            <a class="handle ${'active' if queue_type == ACCEPTED_QUEUE else ''}" href="${url('queue_list', type=ACCEPTED_QUEUE)}" data-target="${ACCEPTED_QUEUE}">${_("Accepted")}</a>
            <a class="handle ${'active' if queue_type == REVIEW_QUEUE else ''}" href="${url('queue_list', type=REVIEW_QUEUE)}" data-target="${REVIEW_QUEUE}">${_("Review")}</a>
        </div>

        <div class="search">
            ${h.form('get', action=url('queue_list'))}
                ${h.HIDDEN('type', queue_type)}
                ${h.vinput('query', locals(), _placeholder=_("Search"))}
                <button type="submit"></button>
            </form>
        </div>

        <div class="queue ${queue_type}" data-source="${queue_type}">
            ${queue_list.body()}
        </div>

        <div class="queue ${hidden_queue_type} hidden" data-source="${hidden_queue_type}"></div>
    </div>
</%block>

<%block name="extra_body">
    <script type="text/template" id="queueLoadError">
        <p>${_('Queue loading failed. Please try again in a few seconds.')}</p>
    </script>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/queue']}"></script>
</%block>
