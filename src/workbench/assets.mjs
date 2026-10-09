// Adapt the historical, contributed-photo and narrative manifest shapes at the
// consumer boundary. Preserve IDs, hashes and evidence classification verbatim.
export function normalizeAsset(asset) {
  const archivePath = asset.archive?.path || asset.archive_path || asset.path;
  return {
    ...asset,
    filename: asset.filename || asset.uploaded_name || archivePath?.split('/').at(-1) || '',
    archive: archivePath ? {...asset.archive, path: archivePath} : null,
  };
}
export function isImageAsset(asset) {
  return !!asset?.archive?.path && /\.(jpe?g|png|webp)$/i.test(asset.filename);
}
