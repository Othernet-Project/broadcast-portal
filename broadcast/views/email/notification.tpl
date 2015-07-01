There are ${len(content)} new content broadcast and ${len(twitter)} new twitter broadcast requests.

% if content:
    List of content broadcast requests:
    % for item in content:
    ${item.id}
    % endfor
% endif

% if twitter:
    List of twitter broadcast requests:
    % for item in twitter:
    ${item.id}
    % endfor
% endif
