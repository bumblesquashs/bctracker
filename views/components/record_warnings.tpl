% if len(record.warnings) > 0:
    <div class="tooltip-anchor record-warnings">
        % include('components/svg', name='warning')
        <div class="tooltip right">
            <div class="title">Potential accidental login</div>
            % for warning in record.warnings:
                <div>{{ warning }}</div>
            % end
        </div>
    </div>
% end
