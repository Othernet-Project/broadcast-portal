<%inherit file='base.tpl'/>
<%namespace name="queue_list" file="_queue_list.tpl"/>

<%block name="main">
    <div class="bin-status">
        <h1>${_("Daily Bin")}</h1>
        <p>
            <span class="bin-usage-data">${_("Current bin size: {size} / {usage}%".format(size=h.hsize(bin.size), usage=bin.usage))}</span>
            <span>${_("Broadcasting in: ")}</span>
        </p>
        <span class="bin-usage-bar">
            <span class="bin-usage-bar-indicator" style="width: ${bin.usage}%"></span>
        </span>
    </div>

    <div class="handles">
        <a class="handle" href="${url('queue_list', type=ACCEPTED_QUEUE)}" data-target="${ACCEPTED_QUEUE}">${_("Accepted")}</a>
        <a class="handle" href="${url('queue_list', type=REVIEW_QUEUE)}" data-target="${REVIEW_QUEUE}">${_("Review")}</a>
    </div>

    <div class="search">
        ${h.form('get', action=url('queue_list', type=queue_type))}
            <input type="text" name="query" />
            <button type="submit"></button>
        </form>
    </div>

    <div class="queue ${queue_type}">
        ${queue_list.body()}
    </div>

    <div class="queue ${hidden_queue_type} hidden"></div>
</%block>

<%block name="extra_body">
    <script type="text/template" id="queueLoadError">
        <p>${_('Queue loading failed. Please try again in a few seconds.')}</p>
    </script>
</%block>

<%block name="extra_scripts">
    <script src="${assets['js/queue']}"></script>
</%block>
